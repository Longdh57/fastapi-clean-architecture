from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.library import Library
from app.domain.entities.library_book import LibraryBook


class LibraryRepository(ABC):
    """Repository interface (port) for libraries and their book holdings."""

    # --- Library CRUD ---
    @abstractmethod
    def add(self, library: Library) -> Library:
        ...

    @abstractmethod
    def get_by_id(self, library_id: int) -> Optional[Library]:
        ...

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[Library]:
        ...

    @abstractmethod
    def update(self, library: Library) -> Library:
        ...

    @abstractmethod
    def delete(self, library_id: int) -> None:
        ...

    # --- Library <-> Book holdings (many-to-many with quantity) ---
    @abstractmethod
    def get_holding(self, library_id: int, book_id: int) -> Optional[LibraryBook]:
        ...

    @abstractmethod
    def set_holding(self, library_id: int, book_id: int, quantity: int) -> LibraryBook:
        """Create or overwrite the quantity of a book held in a library."""
        ...

    @abstractmethod
    def remove_holding(self, library_id: int, book_id: int) -> None:
        ...

    @abstractmethod
    def list_books_in_library(self, library_id: int) -> List[LibraryBook]:
        """Holdings of one library, each with its resolved Book and quantity."""
        ...

    @abstractmethod
    def list_libraries_of_book(self, book_id: int) -> List[LibraryBook]:
        """Holdings of one book across libraries, each with resolved Library."""
        ...
