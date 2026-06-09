"""Integration tests for BookUseCases.create_book backed by a REAL SQLite DB.

Unlike tests/test_book_use_cases.py (which uses an in-memory dict fake), this
suite wires the actual SQLAlchemyBookRepository to a dedicated database file,
``books1.db`` — separate from the app's ``books.db`` so tests never touch real
data. The file is created fresh and deleted around every test for isolation.
"""

import os
import sqlite3

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.exceptions import DuplicateISBNError
from app.application.use_cases.book_use_cases import BookUseCases
from app.infrastructure.database import models  # noqa: F401  (registers tables)
from app.infrastructure.database.connection import Base
from app.infrastructure.repositories.book_repository_impl import (
    SQLAlchemyBookRepository,
)

TEST_DB_PATH = "books1.db"
TEST_DB_URL = f"sqlite:///./{TEST_DB_PATH}"


@pytest.fixture
def engine():
    """A fresh SQLite engine + schema on books1.db, torn down afterwards."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)


@pytest.fixture
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture
def use_cases(session_factory):
    """Use cases wired to the REAL repository against books1.db."""
    session = session_factory()
    try:
        yield BookUseCases(SQLAlchemyBookRepository(session))
    finally:
        session.close()


class TestCreateBookWithDatabase:
    def test_db_file_is_created(self, use_cases):
        use_cases.create_book(
            title="Clean Architecture",
            author="Robert C. Martin",
            isbn="9780134494166",
            published_year=2017,
        )
        # The data really landed in a file on disk, not just memory.
        assert os.path.exists(TEST_DB_PATH)

    def test_creates_book_and_returns_entity_with_generated_id(self, use_cases):
        book = use_cases.create_book(
            title="Refactoring",
            author="Martin Fowler",
            isbn="9780134757599",
            published_year=2018,
            description="Improving the design of existing code",
        )

        assert book.id is not None
        assert book.title == "Refactoring"
        # Timestamps are filled by the DB server_default — proof the row was written.
        assert book.created_at is not None
        assert book.updated_at is not None

    def test_row_is_persisted_and_readable_from_a_separate_session(
        self, use_cases, session_factory
    ):
        created = use_cases.create_book(
            title="Domain-Driven Design",
            author="Eric Evans",
            isbn="9780321125217",
            published_year=2003,
        )

        # Open an INDEPENDENT session and read it back — proves it hit the DB,
        # not some in-process cache.
        other_session = session_factory()
        try:
            repo = SQLAlchemyBookRepository(other_session)
            fetched = repo.get_by_id(created.id)
        finally:
            other_session.close()

        assert fetched is not None
        assert fetched.isbn == "9780321125217"

    def test_row_exists_when_querying_books1_db_with_raw_sqlite(self, use_cases):
        use_cases.create_book(
            title="The Pragmatic Programmer",
            author="Andrew Hunt",
            isbn="9780201616224",
            published_year=1999,
        )

        # Bypass SQLAlchemy entirely and read the raw file with sqlite3.
        conn = sqlite3.connect(TEST_DB_PATH)
        try:
            rows = conn.execute(
                "SELECT title, isbn FROM books WHERE isbn = ?", ("9780201616224",)
            ).fetchall()
        finally:
            conn.close()

        assert rows == [("The Pragmatic Programmer", "9780201616224")]

    def test_duplicate_isbn_is_rejected_against_real_db(self, use_cases):
        use_cases.create_book(
            title="Original", author="A", isbn="9781234567897", published_year=2010
        )

        with pytest.raises(DuplicateISBNError):
            use_cases.create_book(
                title="Copycat", author="B", isbn="9781234567897", published_year=2011
            )

        # Confirm only one row really exists in the file.
        conn = sqlite3.connect(TEST_DB_PATH)
        try:
            (count,) = conn.execute(
                "SELECT COUNT(*) FROM books WHERE isbn = ?", ("9781234567897",)
            ).fetchone()
        finally:
            conn.close()
        assert count == 1

    def test_unique_constraint_blocks_duplicate_isbn_at_db_level(
        self, use_cases, session_factory
    ):
        """Even bypassing the use case, the DB's UNIQUE(isbn) index holds."""
        use_cases.create_book(
            title="First", author="A", isbn="9789999999999", published_year=2000
        )

        from sqlalchemy.exc import IntegrityError

        from app.infrastructure.database.models import BookModel

        rogue_session = session_factory()
        try:
            rogue_session.add(
                BookModel(
                    title="Sneaky",
                    author="B",
                    isbn="9789999999999",  # same ISBN, inserted directly
                    published_year=2001,
                )
            )
            with pytest.raises(IntegrityError):
                rogue_session.commit()
        finally:
            rogue_session.rollback()
            rogue_session.close()
