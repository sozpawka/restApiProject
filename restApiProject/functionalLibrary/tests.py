from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status

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


# логика художественная/учебник
class CategoryValidationTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Автор 1")

    def test_textbook_unique_rules(self):
        """
        Учебник: нельзя создать одинаковый год + издательство.
        """
        Book.objects.create(
            title="Учебник математики",
            author=self.author,
            publication_year=2010,
            genre="Учебник",
            category="учебник",
            publisher="Просвещение"
        )

        duplicate = Book(
            title="Учебник математики",
            author=self.author,
            publication_year=2010,
            genre="Учебник",
            category="учебник",
            publisher="Просвещение"
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

# корректное создание книги
class BookCreateTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Автор 1")

    def test_book_create_success(self):
        """Проверка успешного создания книги"""
        book = Book(
            title="Новая книга",
            author=self.author,
            publication_year=2022,
            genre="Роман",
            category="художественное",
            publisher="Эксмо"
        )
        book.full_clean()
        book.save()

        self.assertEqual(Book.objects.count(), 1)



#  поиск через api
class BookAPISearchTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Толстой")

        Book.objects.create(
            title="Война и мир",
            author=self.author,
            publication_year=1869,
            genre="Роман",
            category="художественное",
            publisher="АСТ"
        )

    def test_search_by_title(self):
        response = self.client.get("/api/books/?title=Война и мир")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_search_by_genre(self):
        response = self.client.get("/api/books/?genre=Роман")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_search_by_author(self):
        response = self.client.get("/api/books/?author=Толстой")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)