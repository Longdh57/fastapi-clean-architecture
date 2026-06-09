from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.exceptions import BookNotFoundError, DuplicateISBNError
from app.application.use_cases.book_use_cases import BookUseCases
from app.application.use_cases.library_use_cases import LibraryUseCases
from app.presentation.dependencies import get_book_use_cases, get_library_use_cases
from app.presentation.schemas.book import BookCreate, BookResponse, BookUpdate
from app.presentation.schemas.library import (
    LibraryHoldingResponse,
    LibraryResponse,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: BookCreate,
    use_cases: BookUseCases = Depends(get_book_use_cases),
) -> BookResponse:
    try:
        book = use_cases.create_book(
            title=payload.title,
            author=payload.author,
            isbn=payload.isbn,
            published_year=payload.published_year,
            description=payload.description,
        )
    except DuplicateISBNError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return BookResponse.model_validate(book)


@router.get("", response_model=List[BookResponse])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    use_cases: BookUseCases = Depends(get_book_use_cases),
) -> List[BookResponse]:
    books = use_cases.list_books(skip=skip, limit=limit)
    return [BookResponse.model_validate(b) for b in books]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    use_cases: BookUseCases = Depends(get_book_use_cases),
) -> BookResponse:
    try:
        book = use_cases.get_book(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return BookResponse.model_validate(book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    payload: BookUpdate,
    use_cases: BookUseCases = Depends(get_book_use_cases),
) -> BookResponse:
    try:
        book = use_cases.update_book(
            book_id=book_id,
            title=payload.title,
            author=payload.author,
            isbn=payload.isbn,
            published_year=payload.published_year,
            description=payload.description,
        )
    except BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except DuplicateISBNError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return BookResponse.model_validate(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    use_cases: BookUseCases = Depends(get_book_use_cases),
) -> None:
    try:
        use_cases.delete_book(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{book_id}/libraries", response_model=List[LibraryHoldingResponse])
def list_libraries_of_book(
    book_id: int,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> List[LibraryHoldingResponse]:
    """List every library that holds this book, with the quantity in each."""
    try:
        holdings = use_cases.list_libraries_of_book(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return [
        LibraryHoldingResponse(
            quantity=h.quantity, library=LibraryResponse.model_validate(h.library)
        )
        for h in holdings
    ]
