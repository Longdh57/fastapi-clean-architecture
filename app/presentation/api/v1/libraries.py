from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.exceptions import (
    BookNotFoundError,
    HoldingNotFoundError,
    LibraryNotFoundError,
)
from app.application.use_cases.library_use_cases import LibraryUseCases
from app.presentation.dependencies import get_library_use_cases
from app.presentation.schemas.book import BookResponse
from app.presentation.schemas.library import (
    BookInLibraryResponse,
    HoldingSet,
    LibraryCreate,
    LibraryResponse,
    LibraryUpdate,
)

router = APIRouter(prefix="/libraries", tags=["libraries"])


@router.post("", response_model=LibraryResponse, status_code=status.HTTP_201_CREATED)
def create_library(
    payload: LibraryCreate,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> LibraryResponse:
    library = use_cases.create_library(
        name=payload.name,
        address=payload.address,
        established_year=payload.established_year,
        description=payload.description,
    )
    return LibraryResponse.model_validate(library)


@router.get("", response_model=List[LibraryResponse])
def list_libraries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> List[LibraryResponse]:
    libraries = use_cases.list_libraries(skip=skip, limit=limit)
    return [LibraryResponse.model_validate(lib) for lib in libraries]


@router.get("/{library_id}", response_model=LibraryResponse)
def get_library(
    library_id: int,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> LibraryResponse:
    try:
        library = use_cases.get_library(library_id)
    except LibraryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return LibraryResponse.model_validate(library)


@router.put("/{library_id}", response_model=LibraryResponse)
def update_library(
    library_id: int,
    payload: LibraryUpdate,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> LibraryResponse:
    try:
        library = use_cases.update_library(
            library_id=library_id,
            name=payload.name,
            address=payload.address,
            established_year=payload.established_year,
            description=payload.description,
        )
    except LibraryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return LibraryResponse.model_validate(library)


@router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_library(
    library_id: int,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> None:
    try:
        use_cases.delete_library(library_id)
    except LibraryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# --- Book holdings within a library ---
@router.get("/{library_id}/books", response_model=List[BookInLibraryResponse])
def list_books_in_library(
    library_id: int,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> List[BookInLibraryResponse]:
    try:
        holdings = use_cases.list_books_in_library(library_id)
    except LibraryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return [
        BookInLibraryResponse(
            quantity=h.quantity, book=BookResponse.model_validate(h.book)
        )
        for h in holdings
    ]


@router.put(
    "/{library_id}/books",
    response_model=BookInLibraryResponse,
    status_code=status.HTTP_200_OK,
)
def set_book_in_library(
    library_id: int,
    payload: HoldingSet,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> BookInLibraryResponse:
    """Add a book to the library or overwrite its quantity."""
    try:
        holding = use_cases.set_book_quantity(
            library_id=library_id, book_id=payload.book_id, quantity=payload.quantity
        )
    except LibraryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return BookInLibraryResponse(
        quantity=holding.quantity, book=BookResponse.model_validate(holding.book)
    )


@router.delete(
    "/{library_id}/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_book_from_library(
    library_id: int,
    book_id: int,
    use_cases: LibraryUseCases = Depends(get_library_use_cases),
) -> None:
    try:
        use_cases.remove_book_from_library(library_id, book_id)
    except (LibraryNotFoundError, HoldingNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
