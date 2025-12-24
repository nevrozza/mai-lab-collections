import random
from enum import Enum, auto

from src.library.book import Book, Genre
from src.library.library import LibraryPanel
from src.simulation.utils import generate_random_book, get_isbn, get_random_title


class Event(Enum):
    ADD_BOOK = auto()
    REMOVE_RANDOM_BOOK = auto()
    SEARCH_BY_AUTHOR = auto()
    SEARCH_BY_YEAR = auto()
    SEARCH_BY_ISBN = auto()
    TRY_ADD_ISBN_DUPLICATE = auto()
    TRY_GET_UNEXISTING_BOOK = auto()
    CHANGE_BOOK_TITLE = auto()
    TRY_REMOVE_UNEXISTING_BOOK = auto()


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

    def _try_get_unexisting_book_handler(self) -> None:
        all_existing_isbns = self.panel.library.get_all_isbns()
        if len(all_existing_isbns) != 100000:  # TODO
            isbn: str = ""
            while isbn in all_existing_isbns:
                isbn = get_isbn()
            self.panel.find_by_isbn(isbn)
        else:
            print("Все ISBN заняты")

    def _change_book_title_handler(self) -> None:
        book = self._unsafe_get_random_existing_book()
        previous_title = book.title
        book.title = get_random_title()
        new_book = self.panel.library.find_by_isbn(book.isbn)
        if new_book:
            print(f"Изменено название книги: {previous_title} -> {new_book.title}")
        else:
            raise RuntimeError("Книга не была найдена (а должна была)")

    def _try_remove_unexisting_book_handler(self) -> None:
        book = generate_random_book()
        self.panel.remove_book(book)

    def _library_not_empty(self) -> bool:  # была бы лямбдой, но MyPy не разрешил =/
        return len(self.panel.library.get_all_isbns()) > 0

    def get_event_handlers(self) -> dict:
        event_handlers = {
            Event.ADD_BOOK: (lambda: True, self._add_book_handler),
            Event.REMOVE_RANDOM_BOOK: (self._library_not_empty, self._remove_random_book_handler),
            Event.SEARCH_BY_AUTHOR: (self._library_not_empty, self._search_by_author_handler),
            Event.SEARCH_BY_YEAR: (self._library_not_empty, self._search_by_year_handler),
            Event.SEARCH_BY_ISBN: (self._library_not_empty, self._search_by_isbn_handler),
            Event.TRY_ADD_ISBN_DUPLICATE: (self._library_not_empty, self._try_add_isbn_duplicate_handler),
            Event.TRY_GET_UNEXISTING_BOOK: (lambda: True, self._try_get_unexisting_book_handler),
            Event.CHANGE_BOOK_TITLE: (self._library_not_empty, self._change_book_title_handler),
            Event.TRY_REMOVE_UNEXISTING_BOOK: (lambda: True, self._try_remove_unexisting_book_handler)
        }
        return event_handlers
