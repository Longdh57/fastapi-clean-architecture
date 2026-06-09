from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Clean Architecture"])
    author: str = Field(..., min_length=1, max_length=255, examples=["Robert C. Martin"])
    isbn: str = Field(..., min_length=1, max_length=20, examples=["9780134494166"])
    published_year: int = Field(..., ge=0, examples=[2017])
    description: Optional[str] = Field(None, examples=["A craftsman's guide to software structure."])


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=1, max_length=20)
    published_year: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
