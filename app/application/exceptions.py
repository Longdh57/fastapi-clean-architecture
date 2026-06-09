class ApplicationError(Exception):
    """Base class for application-level errors."""


class BookNotFoundError(ApplicationError):
    def __init__(self, book_id: int) -> None:
        super().__init__(f"Book with id {book_id} was not found")
        self.book_id = book_id


class DuplicateISBNError(ApplicationError):
    def __init__(self, isbn: str) -> None:
        super().__init__(f"A book with ISBN {isbn} already exists")
        self.isbn = isbn


class LibraryNotFoundError(ApplicationError):
    def __init__(self, library_id: int) -> None:
        super().__init__(f"Library with id {library_id} was not found")
        self.library_id = library_id


class HoldingNotFoundError(ApplicationError):
    def __init__(self, library_id: int, book_id: int) -> None:
        super().__init__(
            f"Book {book_id} is not held in library {library_id}"
        )
        self.library_id = library_id
        self.book_id = book_id
