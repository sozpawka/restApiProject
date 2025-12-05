from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "birth_date"]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publication_year",
            "genre",
            "category",
            "publisher",
            "cover_image",
            "book_file",
        ]
