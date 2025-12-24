import random

from src.library.book import Genre, Book

_TITLES = [
    "Война и мир", "Преступление и наказание", "Мастер и Маргарита",
    "1984", "Гарри Поттер и философский камень", "Анна Каренина",
    "Три товарища", "О дивный новый мир", "Сто лет одиночества"
]
_AUTHORS = ["Толстой", "Достоевский", "Булгаков", "Оруэлл", "Роулинг", "Ремарк"]
_GENRES = list(Genre)
_ISBNS = [f"ISBN-{i:05d}" for i in range(100000)]  # TODO


def get_isbn() -> str:  # TODO
    return random.choice(_ISBNS)


def get_random_title() -> str:
    return random.choice(_TITLES)


def generate_random_book() -> Book:
    title = f"{random.choice(_TITLES)}"
    author = get_random_title()
    year = random.randint(1800, 2025)
    genre = random.choice(_GENRES)
    isbn = get_isbn()
    return Book(title=title, author=author, year=year, genre=genre, isbn=isbn)
