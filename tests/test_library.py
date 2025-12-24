import sys
from io import StringIO

import pytest

from src.library.book import Book, Genre
from src.library.collections.book_collection import ImmutableBookCollection
from src.library.library import Library, LibraryPanel
from src.simulation.utils import generate_random_book


def test_library_remove_from_dicts():
    lib = Library()
    book1 = Book("A", "X", 2020, Genre.FANTASY, "1")
    book2 = Book("B", "X", 2020, Genre.ROMANCE, "2")  # тот же автор и год

    lib.add_book(book1)
    lib.add_book(book2)

    lib.remove_book(book1)

    by_author = lib.find_by_author("X")
    assert len(by_author) == 1
    assert by_author[0].isbn == "2"

    by_year = lib.find_by_year(2020)
    assert len(by_year) == 1
    assert by_year[0].isbn == "2"

    assert lib.find_by_isbn("1") is None


def test_book_mutability():
    # Мб стоило добавить ImmutableBook или DeepCopy?
    # Т.к. мы возвращаем мутабельный Book и это сокращает заслуги ImmutableBookCollection...
    # После чего добавить методы-ручки для update
    # Но сейчас реализовано иначе
    lib = Library()
    book = generate_random_book()
    lib.add_book(book)
    new_title = "meow"
    book.title = new_title
    book_from_library = lib.find_by_isbn(book.isbn)
    if book_from_library:
        assert new_title == book_from_library.title
    else:
        raise AssertionError


def test_library():
    lib = Library()
    book1 = generate_random_book()
    book2 = generate_random_book()

    lib.add_book(book1)
    lib.add_book(book2)

    assert lib.find_by_isbn(book1.isbn) == book1
    assert lib.find_by_isbn("xxx") is None

    by_author = lib.find_by_author(book1.author)
    assert isinstance(by_author, ImmutableBookCollection)
    assert book1 in by_author

    by_year = lib.find_by_year(book1.year)
    assert isinstance(by_year, ImmutableBookCollection)
    assert book1 in by_year

    duplicate = generate_random_book()
    duplicate.isbn = book1.isbn
    with pytest.raises(KeyError, match="Duplicate book"):
        lib.add_book(duplicate)

    lib.remove_book(book1)
    assert lib.find_by_isbn(book1.isbn) is None
    assert book1 not in lib.find_by_author(book1.author)
    assert book1 not in lib.find_by_year(book1.year)

    with pytest.raises(ValueError):
        lib.remove_book(book1)


def test_library_empty_state():
    lib = Library()
    assert lib.get_all_isbns() == []
    assert lib.find_by_author("Unknown")._books == ()
    assert lib.find_by_year(2025)._books == ()
    assert lib.find_by_isbn("any") is None


def test_library_panel():
    lib = Library()
    panel = LibraryPanel(lib)
    book = generate_random_book()

    panel.add_book(book)
    assert lib.find_by_isbn(book.isbn) is not None

    captured_output = StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured_output
    panel.add_book(book)  # дубликат
    sys.stdout = old_stdout

    output = captured_output.getvalue()
    assert "уже добавлена" in output

    fake_book = generate_random_book()
    captured_output = StringIO()
    sys.stdout = captured_output
    panel.remove_book(fake_book)
    sys.stdout = old_stdout
    assert "Этой книги не существует" in captured_output.getvalue()

    panel.find_by_isbn("missing")  # не падает..

    by_author = panel.find_by_author(book.author)
    assert isinstance(by_author, ImmutableBookCollection)

    by_year = panel.find_by_year(book.year)
    assert isinstance(by_year, ImmutableBookCollection)
