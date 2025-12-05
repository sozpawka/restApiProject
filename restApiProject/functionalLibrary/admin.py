from django.contrib import admin
from .models import Author, Book

# регистрация моделей для отображения в админке
admin.site.register(Author)
admin.site.register(Book)
