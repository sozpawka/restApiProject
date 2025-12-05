from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "birth_date"]


class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "author_id",
            "publication_year", "genre", "category",
            "publisher", "cover_image", "book_file"
        ]

    def create(self, validated_data):
        book = Book(**validated_data)
        try:
            book.full_clean()  # вся логика в модели
            book.save()
            return book
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        except IntegrityError:
            raise serializers.ValidationError("Такая книга уже есть.")

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        try:
            instance.full_clean()
            instance.save()
            return instance
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        except IntegrityError:
            raise serializers.ValidationError("Такая книга уже есть.")
