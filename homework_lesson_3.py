# Система управління бібліотекою...
from pydantic import BaseModel
from abc import ABC, abstractmethod
import os
import json
from typing import List, Generator
from functools import wraps

###########################################################################################
# Створення Pydantic моделі


class BookModel(BaseModel):
    title: str
    author: str
    year: int

###########################################################################################
#Створення Абстрактного класу

class Publication(ABC):
    @abstractmethod
    def info(self) -> str:
        pass

###########################################################################################
# Створення класу Книга, який успадковується від абстрактного класу

class Book(Publication):
    def __init__(self, model: BookModel):
        self.model = model

    def info(self) -> str:
        return f"Книга: {self.model.title}, Автор: {self.model.author}, Рік: {self.model.year}"

###########################################################################################
# Створення класу журнал

class Journal(Book):
    def info(self) -> str:
        return f"Журнал: {self.model.title}, Автор: {self.model.author}, Рік: {self.model.year}"

###########################################################################################
# Створення декораторів логування при додаванні нової книги, та декоратору перевірки
# наявності книги в бібліотеці перед видаленням

def log_addition(func):
    @wraps(func)
    def wrapper(self, item):
        result = func(self, item)
        with open("library.log", "a", encoding="utf-8") as f:
            f.write(f"Додано: {item.info()}\n")
        return result
    return wrapper

def check_exists(func):
    @wraps(func)
    def wrapper(self, title):
        if not any(book.model.title == title for book in self._books):
            print(f"Книга '{title}' не знайдена в бібліотеці.")
            return
        return func(self, title)
    return wrapper

###########################################################################################
# Створення контекстного менеджера

class LibraryContextManager:
    def __init__(self, library, filename="library.json"):
        self.library = library
        self.filename = filename

    def __enter__(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    model = BookModel(**item["data"])
                    if item["type"] == "Journal":
                        book = Journal(model)
                    else:
                        book = Book(model)
                    self.library.add(book)
        return self.library

    def __exit__(self, exc_type, exc_val, exc_tb):
        data = [
            {
                "type": "Journal" if isinstance(book, Journal) else "Book",
                "data": book.model.model_dump()
            }
            for book in self.library._books
        ]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

###########################################################################################
# Створення класу Бібліотека

class Library:
    def __init__(self):
        self._books: List[Publication] = []

    def __iter__(self):
        return iter(self._books)

    def books_by_author(self, author: str) -> Generator[Publication, None, None]:
        return (book for book in self._books if book.model.author == author)

    @log_addition
    def add(self, item: Publication):
        self._books.append(item)

    @check_exists
    def remove(self, title: str):
        self._books = [book for book in self._books if book.model.title != title]

    def list_books(self):
        for book in self._books:
            print(book.info())

# -------------------------------
# Демонстрація
# -------------------------------

# Інстанси книги та журналу
book_model_1 = BookModel(title="Book_1", author="author_1", year=2000)
book_model_2 = BookModel(title="Book_2", author="author_2", year=2008)
book_model_3 = BookModel(title="Book_3", author="author_1", year=2010)
book1 = Book(book_model_1)
book2 = Book(book_model_2)
book3 = Book(book_model_3)


journal_model_1 = BookModel(title="Journal_1", author="author_1", year=2001)
journal_model_2 = BookModel(title="Journal_2", author="author_2", year=2005)
journal_1 = Journal(journal_model_1)
journal_2 = Journal(journal_model_2)

# Створення бібліотеки
library = Library()

# Додавання
library.add(book1)
library.add(book2)
library.add(book3)
library.add(journal_1)
library.add(journal_2)

print("\n Список книг у бібліотеці:")
library.list_books()

print("\n Книги автора author_1:")
for item in library.books_by_author("author_1"):
    print(item.info())

# Видалення
library.remove("Journal_1")
print("\n Список після видалення:")
library.list_books()

# Збереження до файлу
with LibraryContextManager(library):
    pass

# Створення нової бібліотеки та завантаження з файлу
print("\n Завантаження бібліотеки з файлу:")
new_library = Library()
with LibraryContextManager(new_library):
    new_library.list_books()