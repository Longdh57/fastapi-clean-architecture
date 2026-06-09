from typing import List, Optional

from app.application.exceptions import (
    BookNotFoundError,
    HoldingNotFoundError,
    LibraryNotFoundError,
)
from app.domain.entities.library import Library
from app.domain.entities.library_book import LibraryBook
from app.domain.repositories.book_repository import BookRepository
from app.domain.repositories.library_repository import LibraryRepository


class LibraryUseCases:
    """Application business rules for libraries and their book holdings.
    Composes the library and book repository ports."""

    def __init__(
        self,
        library_repository: LibraryRepository,
        book_repository: BookRepository,
    ) -> None:
        self._libraries = library_repository
        self._books = book_repository

    # --- Library CRUD ---
    def create_library(
        self,
        name: str,
        address: str,
        established_year: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Library:
        library = Library(
            name=name,
            address=address,
            established_year=established_year,
            description=description,
        )
        return self._libraries.add(library)

    def get_library(self, library_id: int) -> Library:
        library = self._libraries.get_by_id(library_id)
        if library is None:
            raise LibraryNotFoundError(library_id)
        return library

    def list_libraries(self, skip: int = 0, limit: int = 100) -> List[Library]:
        return self._libraries.list(skip=skip, limit=limit)

    def update_library(
        self,
        library_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        established_year: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Library:
        library = self._libraries.get_by_id(library_id)
        if library is None:
            raise LibraryNotFoundError(library_id)

        if name is not None:
            library.name = name
        if address is not None:
            library.address = address
        if established_year is not None:
            library.established_year = established_year
        if description is not None:
            library.description = description

        return self._libraries.update(library)

    def delete_library(self, library_id: int) -> None:
        library = self._libraries.get_by_id(library_id)
        if library is None:
            raise LibraryNotFoundError(library_id)
        self._libraries.delete(library_id)

    # --- Book holdings (many-to-many with quantity) ---
    def _ensure_library(self, library_id: int) -> None:
        if self._libraries.get_by_id(library_id) is None:
            raise LibraryNotFoundError(library_id)

    def _ensure_book(self, book_id: int) -> None:
        if self._books.get_by_id(book_id) is None:
            raise BookNotFoundError(book_id)

    def set_book_quantity(
        self, library_id: int, book_id: int, quantity: int
    ) -> LibraryBook:
        """Add a book to a library or overwrite its quantity."""
        self._ensure_library(library_id)
        self._ensure_book(book_id)
        return self._libraries.set_holding(library_id, book_id, quantity)

    def remove_book_from_library(self, library_id: int, book_id: int) -> None:
        self._ensure_library(library_id)
        if self._libraries.get_holding(library_id, book_id) is None:
            raise HoldingNotFoundError(library_id, book_id)
        self._libraries.remove_holding(library_id, book_id)

    def list_books_in_library(self, library_id: int) -> List[LibraryBook]:
        self._ensure_library(library_id)
        return self._libraries.list_books_in_library(library_id)

    def list_libraries_of_book(self, book_id: int) -> List[LibraryBook]:
        self._ensure_book(book_id)
        return self._libraries.list_libraries_of_book(book_id)
