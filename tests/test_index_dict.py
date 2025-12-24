import pytest

from src.library.book import Genre, Book
from src.library.collections.index_dict import IndexDict
from src.simulation.utils import generate_random_book


def test_index_dict_initial_state():
    idx = IndexDict()
    assert idx.get_all_isbns() == []
    assert idx.get_by_isbn("xxx") is None
    assert len(idx.get_by_author("xxx")) == 0
    assert len(idx.get_by_year(2077)) == 0


def test_index_dict_add_books():
    idx = IndexDict()
    isbnx = idx._via_isbn
    books = [generate_random_book() for _ in range(3)]
    for book in books:
        idx.add_book(book)

    assert len(isbnx) == 3
    total_author = sum(len(v) for v in idx._via_author.values())
    total_year = sum(len(v) for v in idx._via_year.values())
    assert total_author == 3
    assert total_year == 3
    assert idx.get_all_isbns() == list(isbnx.keys())


def test_index_dict_remove_book():
    idx = IndexDict()
    book = generate_random_book()
    idx.add_book(book)

    retrieved = idx.get_by_isbn(book.isbn)
    assert retrieved == book
    assert book in idx.get_by_author(book.author)
    assert book in idx.get_by_year(book.year)

    idx.remove_book(book)
    assert idx.get_by_isbn(book.isbn) is None
    assert book not in idx.get_by_author(book.author)
    assert book not in idx.get_by_year(book.year)


def test_index_dict_clean_keys_on_last_removal():
    idx = IndexDict()
    book = Book("Test", "xxx", 2077, Genre.POETRY, "123")
    idx.add_book(book)

    assert book.author in idx._via_author
    assert book.year in idx._via_year
    assert book.isbn in idx._via_isbn

    idx.remove_book(book)
    assert book.author not in idx._via_author
    assert book.year not in idx._via_year
    assert book.isbn not in idx._via_isbn


def test_index_dict_remove_nonexistent_book_error():
    idx = IndexDict()
    book = generate_random_book()
    for _ in range(2):
        idx.add_book(book)
    for _ in range(2):
        idx.remove_book(book)
    assert book.author not in idx._via_author
    if isinstance(idx._via_author[book.author], list):  # работает из-за default value
        with pytest.raises(ValueError):
            idx.remove_book(book)
