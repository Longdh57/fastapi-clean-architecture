from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    """Core domain entity. Pure Python — no framework or DB dependencies."""

    title: str
    author: str
    isbn: str
    published_year: int
    id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Enforce the entity's invariants. Called on construction and must be
        re-run after any mutation so updates can't bypass the rules."""
        if not self.title or not self.title.strip():
            raise ValueError("Book title must not be empty")
        if not self.author or not self.author.strip():
            raise ValueError("Book author must not be empty")
        if self.published_year < 0:
            raise ValueError("Published year must be a positive number")
