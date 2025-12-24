from abc import abstractmethod, ABC

from src.library.book import Book
from src.library.collections.book_collection import BookCollection, ImmutableBookCollection
from src.library.collections.index_dict import IndexDict


class LibraryABC(ABC):
    @abstractmethod
    def add_book(self, book: Book): ...

    @abstractmethod
    def remove_book(self, book: Book): ...

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Book | None: ...

    @abstractmethod
    def find_by_author(self, author: str) -> ImmutableBookCollection: ...

    @abstractmethod
    def find_by_year(self, year: int) -> ImmutableBookCollection: ...


class Library(LibraryABC):
    def __init__(self):
        self._books = BookCollection()
        self._indexes = IndexDict()

    def add_book(self, book: Book):
        self._indexes.add_book(book)  # можно словить KeyError
        self._books.add(book)

    def remove_book(self, book: Book):
        self._books.remove(book)
        self._indexes.remove_book(book)

    def find_by_isbn(self, isbn: str) -> Book | None:
        return self._indexes.get_by_isbn(isbn)

    def find_by_author(self, author: str) -> ImmutableBookCollection:
        return self._indexes.get_by_author(author)

    def find_by_year(self, year: int) -> ImmutableBookCollection:
        return self._indexes.get_by_year(year)

    def __repr__(self) -> str:
        return f"Library(books={len(self._books)}, indexes={self._indexes})"

    def __str__(self) -> str:
        return f"Библиотека содержит {len(self._books)} книг."


class LibraryPanel(LibraryABC):
    def __init__(self, library: Library):
        self._library = library

    def add_book(self, book: Book):
        pass

    def remove_book(self, book: Book):
        pass

    def find_by_isbn(self, isbn: str) -> Book | None:
        return None

    def find_by_author(self, author: str) -> ImmutableBookCollection:
        return ImmutableBookCollection()

    def find_by_year(self, year: int) -> ImmutableBookCollection:
        return ImmutableBookCollection()
