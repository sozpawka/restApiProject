from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Author, Book

# уникальность книги
class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Автор 1")
        self.book_data = {
            "title": "Книга",
            "author": self.author,
            "publication_year": 2020,
            "genre": "Роман",
            "category": "художественное",
            "publisher": "Издательство А"
        }

    def test_duplicate_book(self):
        # проверка создать книгу-дубликат
        Book.objects.create(**self.book_data)

        duplicate = Book(**self.book_data)

        with self.assertRaises(ValidationError):
            duplicate.full_clean()



# уникальность автора
class AuthorModelTest(TestCase):
    def test_duplicate_author(self):
        # проверка автор не может повторяться
        Author.objects.create(name="Пушкин")
        a2 = Author(name="Пушкин")

        with self.assertRaises(ValidationError):
            a2.full_clean()
