import pytest

from src.library.collections.book_collection import BookCollection, ImmutableBookCollection
from src.simulation.utils import generate_random_book


def test_book_collection_initial_state():
    bc = BookCollection()
    assert len(bc) == 0
    assert isinstance(bc._books, list)


def test_book_collection_add_and_convert_to_immutable():
    bc = BookCollection()
    books = [generate_random_book() for _ in range(3)]
    for book in books:
        bc.add(book)
    imbc = bc.as_immutable()

    bc.add(generate_random_book())

    assert len(bc) == 4
    assert len(imbc) == 3
    assert isinstance(imbc, ImmutableBookCollection)
    assert isinstance(imbc._books, tuple)


def test_book_collection_slicing_returns_immutable():
    bc = BookCollection()
    for _ in range(3):
        bc.add(generate_random_book())
    imbc = bc.as_immutable()

    assert isinstance(bc[1:2], ImmutableBookCollection)
    assert isinstance(imbc[1:2], ImmutableBookCollection)
    assert list(bc[1:2]) == bc._books[1:2]
    assert tuple(imbc[1:2]) == imbc._books[1:2]


def test_book_collection_empty_slices():
    bc = BookCollection()
    imbc = ImmutableBookCollection()

    assert isinstance(bc[100:200], ImmutableBookCollection)
    assert len(bc[100:200]) == 0
    assert isinstance(imbc[5:10], ImmutableBookCollection)
    assert len(imbc[5:10]) == 0


def test_book_collection_remove():
    bc = BookCollection()
    books = [generate_random_book() for _ in range(3)]
    for b in books:
        bc.add(b)

    bc.remove(books[0])
    assert len(bc) == 2

    for book in bc.as_immutable():  # иначе проблема с редактированием mutable во время прохода по ним
        bc.remove(book)
    assert len(bc) == 0

    with pytest.raises(ValueError):
        bc.remove(books[1])
