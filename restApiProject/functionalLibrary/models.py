from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    # имя автора уникальное, двух одинаковых быть не должно
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    # модель книги. запись должна быть уникальна по (title, author, year, publisher)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # художественное / учебник
    publisher = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    book_file = models.FileField(upload_to="books/", blank=True, null=True)

    class Meta:
        unique_together = ('title', 'author', 'publication_year', 'publisher')
        ordering = ['title', 'publication_year']

    def clean(self):
        # базовая проверка года (на всякий случай, хотя есть валидаторы)
        if not (1000 <= self.publication_year <= 9999):
            raise ValidationError("Год выпуска должен быть от 1000 до 9999.")

        # проверяем уникальность записи
        exists = Book.objects.exclude(pk=self.pk).filter(
            title=self.title,
            author=self.author,
            publication_year=self.publication_year,
            publisher=self.publisher,
        )
        if exists.exists():
            raise ValidationError("Такая книга уже существует.")

        # логика для учебников
        if self.category.lower() == "учебник":
            duplicate_textbook = Book.objects.exclude(pk=self.pk).filter(
                title=self.title,
                author=self.author,
                category__iexact="учебник",
                publication_year=self.publication_year,
                publisher=self.publisher,
            )
            if duplicate_textbook.exists():
                raise ValidationError("Учебник с таким же годом и издателем уже есть.")

    def __str__(self):
        return f"{self.title} — {self.author.name} ({self.publication_year})"
