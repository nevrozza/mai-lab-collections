from abc import abstractmethod, ABC

from src.library.book import Book
from src.library.collections.book_collection import BookCollection, ImmutableBookCollection
from src.library.collections.index_dict import IndexDict


class LibraryABC(ABC):
    """Абстрактный интерфейс библиотеки (единообразие Library и LibraryPanel)"""
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
    """
    Основная реализация библиотеки.

    Хранит книги и поддерживает индексы по ISBN, автору и году.
    Запрещает дубликаты ISBN.
    """
    def __init__(self):
        self._books = BookCollection()
        self._indexes = IndexDict()

    def add_book(self, book: Book):
        if book.isbn in self._indexes.get_all_isbns():
            raise KeyError(f"Duplicate book: {book}")
        self._books.add(book)
        self._indexes.add_book(book)

    def remove_book(self, book: Book):
        self._books.remove(book)
        self._indexes.remove_book(book)

    def find_by_isbn(self, isbn: str) -> Book | None:
        return self._indexes.get_by_isbn(isbn)

    def find_by_author(self, author: str) -> ImmutableBookCollection:
        return self._indexes.get_by_author(author)

    def find_by_year(self, year: int) -> ImmutableBookCollection:
        return self._indexes.get_by_year(year)

    def get_all_isbns(self) -> list[str]:
        return self._indexes.get_all_isbns()


class LibraryPanel(LibraryABC):
    """
    Обёртка над Library с обработкой ошибок и выводом сообщений. Что-то типа интерфейса, если бы это было CLI.

    Не выбрасывает исключения при ожидаемых ошибках (дубликат, отсутствующая книга),
    а вместо этого печатает понятные сообщения.
    """
    def __init__(self, library: Library):
        self.library = library

    def add_book(self, book: Book):
        try:
            self.library.add_book(book)
            print(f"Добавлена книга: {book.title}")
        except KeyError:
            print(f"Книга с таким ISBN: {book.isbn} уже добавлена")

    def remove_book(self, book: Book):
        try:
            self.library.remove_book(book)
            print(f"Удалена книга: {book.title}")
        except ValueError:
            print("Этой книги не существует, чтобы удалить её 0_о")

    def find_by_isbn(self, isbn: str) -> Book | None:
        book = self.library.find_by_isbn(isbn)
        if book:
            print(f"Найдена книга по ISBN: {book.title}")
        else:
            print("Книги с таким ISBN не найдено")
        return book

    def find_by_author(self, author: str) -> ImmutableBookCollection:
        books = self.library.find_by_author(author)
        if books:
            print(f"Книги этого автора: {[book.title for book in books]}")
        else:
            print("Похоже, автор пока не нашёл свою музу...")
        return books

    def find_by_year(self, year: int) -> ImmutableBookCollection:
        books = self.library.find_by_year(year)
        if books:
            print(f"Книги {year} года: {[book.title for book in books]}")
        else:
            print("Похоже, в тот год что-то произошло (Книги не найдены)")
        return books
