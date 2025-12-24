from collections.abc import Sequence
from typing import overload

from src.library.book import Book


class BookCollection(Sequence):

    def __init__(self, books=None):
        self._books: list[Book] = books or []

    def add(self, book: Book):
        self._books.append(book)

    def remove(self, book: Book):
        self._books.remove(book)

    @overload
    def __getitem__(self, index: int, /) -> Book: ...

    @overload
    def __getitem__(self, index: slice, /) -> BookCollection: ...

    def __getitem__(self, index: int | slice) -> Book | BookCollection:
        if isinstance(index, slice):
            return BookCollection(self._books[index])  # return no list anymore! (only book_collection)
        return self._books[index]

    def __len__(self) -> int:
        return len(self._books)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._books})"
