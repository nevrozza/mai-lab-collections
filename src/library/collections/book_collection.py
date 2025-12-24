from abc import abstractmethod, ABC
from collections.abc import Sequence
from typing import overload

from src.library.book import Book


class BaseBookCollection(Sequence, ABC):
    _books: Sequence[Book]

    @abstractmethod
    def _make_sliced(self, books_slice: Sequence[Book]) -> BaseBookCollection:
        raise NotImplementedError

    # Кринжанул после котлина (про перегруз методов)
    @overload
    def __getitem__(self, index: int, /) -> Book: ...

    @overload
    def __getitem__(self, index: slice, /) -> BaseBookCollection: ...

    def __getitem__(self, index: int | slice) -> Book | BaseBookCollection:
        if isinstance(index, slice):
            return self._make_sliced(self._books[index])  # return no list anymore! (only BookCollection)
        return self._books[index]

    def __len__(self) -> int:
        return len(self._books)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._books})"


class ImmutableBookCollection(BaseBookCollection):
    def __init__(self, books: None | Sequence[Book] = None):
        self._books: Sequence[Book] = tuple(books) if books else ()

    def _make_sliced(self, books_slice: Sequence[Book]) -> ImmutableBookCollection:
        return ImmutableBookCollection(books_slice)


class BookCollection(BaseBookCollection):
    def __init__(self):
        self._books: list[Book] = []

    def _make_sliced(self, books_slice: Sequence[Book]) -> ImmutableBookCollection:
        return ImmutableBookCollection(books_slice)

    def add(self, book: Book):
        self._books.append(book)

    def remove(self, book: Book):
        self._books.remove(book)

    def as_immutable(self) -> ImmutableBookCollection:
        return ImmutableBookCollection(self._books)
