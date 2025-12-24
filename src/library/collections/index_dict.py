from collections import defaultdict

from src.library.book import Book
from src.library.collections.book_collection import ImmutableBookCollection


class IndexDict:
    def __init__(self):
        self._via_isbn: defaultdict[str, Book] = defaultdict()
        self._via_author: dict[str, list[Book]] = defaultdict(list)
        self._via_year: dict[int, list[Book]] = defaultdict(list)

    def add_book(self, book: Book) -> None:
        if book not in self._via_isbn:
            self._via_isbn[book.isbn] = book
            self._via_author[book.author].append(book)
            self._via_year[book.year].append(book)
        else:
            raise RuntimeError(f"Duplicate book: {book}")

    def remove_book(self, book: Book) -> None:
        dict_and_keys: list[tuple[dict, str | int]] = [(self._via_year, book.year), (self._via_isbn, book.isbn),
                                                       (self._via_author, book.author)]
        for d, k in dict_and_keys:
            self._remove_book_and_key_if_needed(d=d, key=k, book=book)

    @staticmethod
    def _remove_book_and_key_if_needed(d: dict, key: str | int, book: Book) -> None:
        if key in d:
            if isinstance(d[key], list):
                d[key].remove(book)
                if d[key]:
                    return  # Если что-то осталось в списке: оставляем ключ
            del d[key]  # Иначе удаляем его

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self._via_isbn.get(isbn)

    def get_by_author(self, author: str) -> ImmutableBookCollection:
        return ImmutableBookCollection(self._via_author.get(author, []))

    def get_by_year(self, year: int) -> ImmutableBookCollection:
        return ImmutableBookCollection(self._via_year.get(year, []))

    def __getitem__(self, key: str | int) -> Book | ImmutableBookCollection:
        if isinstance(key, str):
            if key in self._via_isbn:
                return self._via_isbn[key]
            elif key in self._via_author:
                return ImmutableBookCollection(self._via_author[key])
        elif isinstance(key, int):
            if key in self._via_year:
                return ImmutableBookCollection(self._via_year[key])
        raise KeyError(f"Key {key} not found.")
