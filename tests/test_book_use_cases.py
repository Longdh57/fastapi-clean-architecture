import pytest

from app.application.exceptions import BookNotFoundError, DuplicateISBNError
from app.application.use_cases.book_use_cases import BookUseCases
from app.domain.entities.book import Book
from tests.fakes import InMemoryBookRepository


@pytest.fixture
def repository() -> InMemoryBookRepository:
    return InMemoryBookRepository()


@pytest.fixture
def use_cases(repository: InMemoryBookRepository) -> BookUseCases:
    return BookUseCases(repository)


class TestCreateBook:
    def test_creates_book_and_returns_entity_with_id(self, use_cases):
        book = use_cases.create_book(
            title="Clean Architecture",
            author="Robert C. Martin",
            isbn="9780134494166",
            published_year=2017,
            description="Software structure guide",
        )

        assert isinstance(book, Book)
        assert book.id == 1
        assert book.title == "Clean Architecture"
        assert book.author == "Robert C. Martin"
        assert book.isbn == "9780134494166"
        assert book.published_year == 2017
        assert book.description == "Software structure guide"

    def test_persists_book_in_repository(self, use_cases, repository):
        created = use_cases.create_book(
            title="Refactoring",
            author="Martin Fowler",
            isbn="9780134757599",
            published_year=2018,
        )

        stored = repository.get_by_id(created.id)
        assert stored is not None
        assert stored.isbn == "9780134757599"

    def test_description_is_optional(self, use_cases):
        book = use_cases.create_book(
            title="Code Complete",
            author="Steve McConnell",
            isbn="9780735619678",
            published_year=2004,
        )

        assert book.description is None

    def test_assigns_incrementing_ids(self, use_cases):
        first = use_cases.create_book(
            title="Book A", author="A", isbn="111", published_year=2000
        )
        second = use_cases.create_book(
            title="Book B", author="B", isbn="222", published_year=2001
        )

        assert first.id == 1
        assert second.id == 2

    def test_duplicate_isbn_raises_and_does_not_persist(self, use_cases, repository):
        use_cases.create_book(
            title="Original", author="A", isbn="9781234567897", published_year=2010
        )

        with pytest.raises(DuplicateISBNError) as exc_info:
            use_cases.create_book(
                title="Copycat",
                author="B",
                isbn="9781234567897",
                published_year=2011,
            )

        assert exc_info.value.isbn == "9781234567897"
        # The duplicate must not have been added.
        assert len(repository.list()) == 1

    @pytest.mark.parametrize("bad_title", ["", "   "])
    def test_empty_title_raises_value_error(self, use_cases, bad_title):
        with pytest.raises(ValueError):
            use_cases.create_book(
                title=bad_title,
                author="A",
                isbn="333",
                published_year=2005,
            )

    def test_negative_year_raises_value_error(self, use_cases):
        with pytest.raises(ValueError):
            use_cases.create_book(
                title="Time Traveler",
                author="A",
                isbn="444",
                published_year=-1,
            )


class TestUpdateBook:
    @pytest.fixture
    def existing_book(self, use_cases) -> Book:
        """A book already stored, used as the update target."""
        return use_cases.create_book(
            title="Original Title",
            author="Original Author",
            isbn="9780000000001",
            published_year=2000,
            description="Original description",
        )

    def test_updates_all_fields(self, use_cases, existing_book):
        updated = use_cases.update_book(
            book_id=existing_book.id,
            title="New Title",
            author="New Author",
            isbn="9780000000002",
            published_year=2020,
            description="New description",
        )

        assert updated.id == existing_book.id
        assert updated.title == "New Title"
        assert updated.author == "New Author"
        assert updated.isbn == "9780000000002"
        assert updated.published_year == 2020
        assert updated.description == "New description"

    def test_partial_update_leaves_other_fields_unchanged(
        self, use_cases, existing_book
    ):
        updated = use_cases.update_book(
            book_id=existing_book.id,
            title="Only Title Changed",
        )

        assert updated.title == "Only Title Changed"
        # Everything else stays as it was.
        assert updated.author == "Original Author"
        assert updated.isbn == "9780000000001"
        assert updated.published_year == 2000
        assert updated.description == "Original description"

    def test_no_fields_provided_keeps_book_intact(self, use_cases, existing_book):
        updated = use_cases.update_book(book_id=existing_book.id)

        assert updated.title == "Original Title"
        assert updated.author == "Original Author"
        assert updated.isbn == "9780000000001"
        assert updated.published_year == 2000

    def test_persists_changes_in_repository(
        self, use_cases, repository, existing_book
    ):
        use_cases.update_book(book_id=existing_book.id, title="Persisted Title")

        stored = repository.get_by_id(existing_book.id)
        assert stored.title == "Persisted Title"

    def test_unknown_id_raises_not_found(self, use_cases):
        with pytest.raises(BookNotFoundError) as exc_info:
            use_cases.update_book(book_id=999, title="Ghost")

        assert exc_info.value.book_id == 999

    def test_keeping_same_isbn_is_allowed(self, use_cases, existing_book):
        # Passing the book's own ISBN must not trip the duplicate check.
        updated = use_cases.update_book(
            book_id=existing_book.id,
            isbn="9780000000001",
            published_year=2099,
        )

        assert updated.isbn == "9780000000001"
        assert updated.published_year == 2099

    def test_changing_to_existing_isbn_raises_and_does_not_persist(
        self, use_cases, repository, existing_book
    ):
        other = use_cases.create_book(
            title="Other Book",
            author="Someone",
            isbn="9780000000099",
            published_year=2010,
        )

        with pytest.raises(DuplicateISBNError) as exc_info:
            use_cases.update_book(
                book_id=existing_book.id, isbn="9780000000099"
            )

        assert exc_info.value.isbn == "9780000000099"
        # The target book must keep its original ISBN.
        assert repository.get_by_id(existing_book.id).isbn == "9780000000001"
        # The other book is untouched.
        assert repository.get_by_id(other.id).isbn == "9780000000099"

    def test_changing_to_a_new_unique_isbn_succeeds(self, use_cases, existing_book):
        updated = use_cases.update_book(
            book_id=existing_book.id, isbn="9781111111111"
        )

        assert updated.isbn == "9781111111111"

    def test_invalid_update_raises_value_error(self, use_cases, existing_book):
        with pytest.raises(ValueError):
            use_cases.update_book(book_id=existing_book.id, title="   ")
