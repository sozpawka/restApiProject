from django.db import models
from django.core.exceptions import ValidationError

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    book_file = models.FileField(upload_to="books/", blank=True, null=True)

    class Meta:
        unique_together = ('title', 'author', 'publication_year', 'publisher')

    def clean(self):
        if not (1000 <= self.publication_year <= 9999):
            raise ValidationError("Год выпуска должен быть от 1000 до 9999")

    def __str__(self):
        return f"{self.title} - {self.author.name}"
