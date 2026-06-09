from typing import List, Optional

from app.application.exceptions import BookNotFoundError, DuplicateISBNError
from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository


class BookUseCases:
    """Application business rules. Orchestrates the domain through the
    repository port, staying ignorant of FastAPI and SQLAlchemy."""

    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    def create_book(
        self,
        title: str,
        author: str,
        isbn: str,
        published_year: int,
        description: Optional[str] = None,
    ) -> Book:
        if self._repository.get_by_isbn(isbn) is not None:
            raise DuplicateISBNError(isbn)
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_year=published_year,
            description=description,
        )
        return self._repository.add(book)

    def get_book(self, book_id: int) -> Book:
        book = self._repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        return book

    def list_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self._repository.list(skip=skip, limit=limit)

    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
        isbn: Optional[str] = None,
        published_year: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Book:
        book = self._repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError(book_id)

        if isbn is not None and isbn != book.isbn:
            existing = self._repository.get_by_isbn(isbn)
            if existing is not None and existing.id != book_id:
                raise DuplicateISBNError(isbn)
            book.isbn = isbn

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if published_year is not None:
            book.published_year = published_year
        if description is not None:
            book.description = description

        book.validate()  # re-check invariants after mutation
        return self._repository.update(book)

    def delete_book(self, book_id: int) -> None:
        book = self._repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        self._repository.delete(book_id)
