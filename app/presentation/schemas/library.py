from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.presentation.schemas.book import BookResponse


class LibraryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Central City Library"])
    address: str = Field(..., min_length=1, max_length=500, examples=["123 Main St, Hanoi"])
    established_year: Optional[int] = Field(None, ge=0, examples=[1998])
    description: Optional[str] = Field(None, examples=["The main public library downtown."])


class LibraryCreate(LibraryBase):
    pass


class LibraryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    established_year: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


class LibraryResponse(LibraryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HoldingSet(BaseModel):
    """Request body to add a book to a library or set its quantity."""

    book_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=0, examples=[5])


class BookInLibraryResponse(BaseModel):
    """A book held in a library, together with its quantity there."""

    quantity: int
    book: BookResponse


class LibraryHoldingResponse(BaseModel):
    """A library that holds a given book, together with the quantity."""

    quantity: int
    library: LibraryResponse
