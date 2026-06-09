from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Library:
    """Core domain entity for a library (a physical or logical collection
    that books can belong to). Pure Python — no framework dependencies."""

    name: str
    address: str
    id: Optional[int] = None
    established_year: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Library name must not be empty")
        if not self.address or not self.address.strip():
            raise ValueError("Library address must not be empty")
        if self.established_year is not None and self.established_year < 0:
            raise ValueError("Established year must be a positive number")
