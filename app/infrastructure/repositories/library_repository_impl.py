from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.library import Library
from app.domain.entities.library_book import LibraryBook
from app.domain.repositories.library_repository import LibraryRepository
from app.infrastructure.database.models import (
    LibraryBookModel,
    LibraryModel,
)
from app.infrastructure.repositories.book_repository_impl import (
    SQLAlchemyBookRepository,
)


class SQLAlchemyLibraryRepository(LibraryRepository):
    """Concrete adapter fulfilling the LibraryRepository port via SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: LibraryModel) -> Library:
        return Library(
            id=model.id,
            name=model.name,
            address=model.address,
            established_year=model.established_year,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _holding_to_entity(model: LibraryBookModel) -> LibraryBook:
        return LibraryBook(
            library_id=model.library_id,
            book_id=model.book_id,
            quantity=model.quantity,
            book=SQLAlchemyBookRepository._to_entity(model.book)
            if model.book is not None
            else None,
            library=SQLAlchemyLibraryRepository._to_entity(model.library)
            if model.library is not None
            else None,
        )

    # --- Library CRUD ---
    def add(self, library: Library) -> Library:
        model = LibraryModel(
            name=library.name,
            address=library.address,
            established_year=library.established_year,
            description=library.description,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, library_id: int) -> Optional[Library]:
        model = self._session.get(LibraryModel, library_id)
        return self._to_entity(model) if model else None

    def list(self, skip: int = 0, limit: int = 100) -> List[Library]:
        stmt = select(LibraryModel).offset(skip).limit(limit).order_by(LibraryModel.id)
        return [self._to_entity(m) for m in self._session.scalars(stmt).all()]

    def update(self, library: Library) -> Library:
        model = self._session.get(LibraryModel, library.id)
        if model is None:
            raise ValueError(f"Library with id {library.id} not found")
        model.name = library.name
        model.address = library.address
        model.established_year = library.established_year
        model.description = library.description
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def delete(self, library_id: int) -> None:
        model = self._session.get(LibraryModel, library_id)
        if model is not None:
            self._session.delete(model)  # cascades to holdings
            self._session.commit()

    # --- Holdings ---
    def get_holding(self, library_id: int, book_id: int) -> Optional[LibraryBook]:
        model = self._session.get(LibraryBookModel, (library_id, book_id))
        return self._holding_to_entity(model) if model else None

    def set_holding(self, library_id: int, book_id: int, quantity: int) -> LibraryBook:
        model = self._session.get(LibraryBookModel, (library_id, book_id))
        if model is None:
            model = LibraryBookModel(
                library_id=library_id, book_id=book_id, quantity=quantity
            )
            self._session.add(model)
        else:
            model.quantity = quantity
        self._session.commit()
        self._session.refresh(model)
        return self._holding_to_entity(model)

    def remove_holding(self, library_id: int, book_id: int) -> None:
        model = self._session.get(LibraryBookModel, (library_id, book_id))
        if model is not None:
            self._session.delete(model)
            self._session.commit()

    def list_books_in_library(self, library_id: int) -> List[LibraryBook]:
        stmt = (
            select(LibraryBookModel)
            .where(LibraryBookModel.library_id == library_id)
            .order_by(LibraryBookModel.book_id)
        )
        return [self._holding_to_entity(m) for m in self._session.scalars(stmt).all()]

    def list_libraries_of_book(self, book_id: int) -> List[LibraryBook]:
        stmt = (
            select(LibraryBookModel)
            .where(LibraryBookModel.book_id == book_id)
            .order_by(LibraryBookModel.library_id)
        )
        return [self._holding_to_entity(m) for m in self._session.scalars(stmt).all()]
