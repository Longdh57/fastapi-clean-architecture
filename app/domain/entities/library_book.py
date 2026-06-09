from dataclasses import dataclass
from typing import Optional

from app.domain.entities.book import Book
from app.domain.entities.library import Library


@dataclass
class LibraryBook:
    """Association entity for the many-to-many relationship between a library
    and a book, carrying the quantity of that book held in that library."""

    library_id: int
    book_id: int
    quantity: int

    # Optionally resolved related entities (filled in when listing).
    book: Optional[Book] = None
    library: Optional[Library] = None

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity must not be negative")
