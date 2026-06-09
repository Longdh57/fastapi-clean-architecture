from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.book import Book


class BookRepository(ABC):
    """Repository interface (port). The domain depends on this abstraction,
    not on any concrete database implementation."""

    @abstractmethod
    def add(self, book: Book) -> Book:
        ...

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        ...

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        ...

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[Book]:
        ...

    @abstractmethod
    def update(self, book: Book) -> Book:
        ...

    @abstractmethod
    def delete(self, book_id: int) -> None:
        ...
