from typing import Dict, List, Optional

from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository


class InMemoryBookRepository(BookRepository):
    """A fake BookRepository backed by a dict, for fast use-case unit tests.
    No database involved — the use case only knows the abstract interface."""

    def __init__(self) -> None:
        self._books: Dict[int, Book] = {}
        self._next_id = 1

    def add(self, book: Book) -> Book:
        book.id = self._next_id
        self._next_id += 1
        self._books[book.id] = book
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return next((b for b in self._books.values() if b.isbn == isbn), None)

    def list(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return list(self._books.values())[skip : skip + limit]

    def update(self, book: Book) -> Book:
        self._books[book.id] = book
        return book

    def delete(self, book_id: int) -> None:
        self._books.pop(book_id, None)
