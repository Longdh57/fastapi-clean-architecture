from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository
from app.infrastructure.database.models import BookModel


class SQLAlchemyBookRepository(BookRepository):
    """Concrete adapter that fulfils the BookRepository port using SQLAlchemy.
    Translates between the persistence model and the domain entity."""

    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: BookModel) -> Book:
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            isbn=model.isbn,
            published_year=model.published_year,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def add(self, book: Book) -> Book:
        model = BookModel(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            published_year=book.published_year,
            description=book.description,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, book_id: int) -> Optional[Book]:
        model = self._session.get(BookModel, book_id)
        return self._to_entity(model) if model else None

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        stmt = select(BookModel).where(BookModel.isbn == isbn)
        model = self._session.scalars(stmt).first()
        return self._to_entity(model) if model else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Book]:
        stmt = select(BookModel).offset(skip).limit(limit).order_by(BookModel.id)
        return [self._to_entity(m) for m in self._session.scalars(stmt).all()]

    def update(self, book: Book) -> Book:
        model = self._session.get(BookModel, book.id)
        if model is None:
            raise ValueError(f"Book with id {book.id} not found")
        model.title = book.title
        model.author = book.author
        model.isbn = book.isbn
        model.published_year = book.published_year
        model.description = book.description
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def delete(self, book_id: int) -> None:
        model = self._session.get(BookModel, book_id)
        if model is not None:
            self._session.delete(model)
            self._session.commit()
