import random

import pytest

from src.library.collections.book_collection import BookCollection, ImmutableBookCollection
from src.library.collections.index_dict import IndexDict
from src.simulation.utils import generate_random_book


def test_book_collection():
    bc = BookCollection()
    for _ in range(3):
        bc.add(generate_random_book())
    imbc = bc.as_immutable()
    assert len(bc) == 3

    assert isinstance(bc._books, list)
    assert isinstance(imbc, ImmutableBookCollection)
    assert isinstance(imbc._books, tuple)
    assert isinstance(bc[1:2], ImmutableBookCollection)
    assert isinstance(imbc[1:2], ImmutableBookCollection)
    assert list(bc[1:2]) == bc._books[1:2]
    assert tuple(imbc[1:2]) == imbc._books[1:2]

    bc.remove(random.choice(bc))
    assert len(bc) == 2
    assert len(imbc) == 3
    for book in bc.as_immutable():  # иначе проблема с редактированием mutable во время прохода по ним
        bc.remove(book)
    assert len(bc) == 0
    with pytest.raises(ValueError):
        bc.remove(random.choice(imbc))


def test_index_dict():
    idx = IndexDict()
    isbnx = idx._via_isbn
    authorx = idx._via_author
    yearx = idx._via_year

    def check_len(num: int):
        assert len(isbnx) == num
        assert sum(len(books) for books in authorx.values()) == num
        assert sum(len(books) for books in yearx.values()) == num

    for _ in range(3):
        idx.add_book(generate_random_book())
    check_len(3)

    assert idx.get_all_isbns() == list(isbnx.keys())
    book = idx.get_by_isbn(random.choice(idx.get_all_isbns()))
    if book:
        idx.remove_book(book)
        if isinstance(authorx[book.author], list):
            with pytest.raises(ValueError):
                idx.remove_book(book)
    else:
        raise AssertionError
    check_len(2)

    book = idx.get_by_isbn(random.choice(idx.get_all_isbns()))
    if book:
        assert book in idx.get_by_author(book.author)
        assert book in idx.get_by_year(book.year)
        assert book == idx.get_by_isbn(book.isbn)
    else:
        raise AssertionError
