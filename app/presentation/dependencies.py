from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.book_use_cases import BookUseCases
from app.application.use_cases.library_use_cases import LibraryUseCases
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.repositories.book_repository_impl import (
    SQLAlchemyBookRepository,
)
from app.infrastructure.repositories.library_repository_impl import (
    SQLAlchemyLibraryRepository,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_book_use_cases(db: Session = Depends(get_db)) -> BookUseCases:
    repository = SQLAlchemyBookRepository(db)
    return BookUseCases(repository)


def get_library_use_cases(db: Session = Depends(get_db)) -> LibraryUseCases:
    library_repository = SQLAlchemyLibraryRepository(db)
    book_repository = SQLAlchemyBookRepository(db)
    return LibraryUseCases(library_repository, book_repository)
