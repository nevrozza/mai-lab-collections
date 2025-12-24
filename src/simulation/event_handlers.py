import random
from enum import Enum, auto

from src.library.book import Book, Genre
from src.library.library import LibraryPanel
from src.simulation.utils import generate_random_book


class Event(Enum):
    ADD_BOOK = auto()
    REMOVE_RANDOM_BOOK = auto()
    SEARCH_BY_AUTHOR = auto()
    SEARCH_BY_YEAR = auto()
    SEARCH_BY_ISBN = auto()
    TRY_ADD_ISBN_DUPLICATE = auto()


class SimulationEventHandlers:

    def __init__(self, panel: LibraryPanel):
        self.panel = panel

    def _unsafe_get_random_existing_book(self) -> Book:
        isbn = random.choice(list(self.panel.library.get_all_isbns()))
        book = self.panel.library.find_by_isbn(isbn)
        if book:
            return book
        else:
            raise RuntimeError("Condition `library_not_empty` is broken..")

    def _add_book_handler(self) -> None:
        book = generate_random_book()
        self.panel.add_book(book)

    def _remove_random_book_handler(self) -> None:
        book_to_remove = self._unsafe_get_random_existing_book()
        self.panel.remove_book(book_to_remove)

    def _search_by_author_handler(self) -> None:
        author = self._unsafe_get_random_existing_book().author
        self.panel.find_by_author(author)

    def _search_by_year_handler(self) -> None:
        year = self._unsafe_get_random_existing_book().year
        self.panel.find_by_year(year)

    def _search_by_isbn_handler(self) -> None:
        isbn = self._unsafe_get_random_existing_book().isbn
        self.panel.find_by_isbn(isbn)

    def _try_add_isbn_duplicate_handler(self) -> None:
        existing_book = self._unsafe_get_random_existing_book()
        fake_book = Book(
            title="Поддельная книга",
            author="Коты какие-то",
            year=2025,
            genre=Genre.FANTASY,
            isbn=existing_book.isbn
        )
        self.panel.add_book(fake_book)

    def _library_not_empty(self) -> bool:  # была бы лямбдой, но mypy не разрешил =/
        return len(self.panel.library.get_all_isbns()) > 0

    def get_event_handlers(self) -> dict:
        event_handlers = {
            Event.ADD_BOOK: (lambda: True, self._add_book_handler),
            Event.REMOVE_RANDOM_BOOK: (self._library_not_empty, self._remove_random_book_handler),
            Event.SEARCH_BY_AUTHOR: (self._library_not_empty, self._search_by_author_handler),
            Event.SEARCH_BY_YEAR: (self._library_not_empty, self._search_by_year_handler),
            Event.SEARCH_BY_ISBN: (self._library_not_empty, self._search_by_isbn_handler),
            Event.TRY_ADD_ISBN_DUPLICATE: (self._library_not_empty, self._try_add_isbn_duplicate_handler)
        }
        return event_handlers
