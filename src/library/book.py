from dataclasses import dataclass
from enum import Enum


class Genre(str, Enum):
    FANTASY = "Фэнтези"
    ROMANCE = "Романы"
    SCIENTIFIC = "Научное"
    ADVENTURE = "Приключения"
    DETECTIVE = "Детектив"
    NON_FICTION = "Публицистика"
    POETRY = "Поэзия"

    def __repr__(self):
        return f"'{self.value}'"


@dataclass
class Book:
    title: str
    author: str
    year: int
    genre: Genre
    isbn: str
