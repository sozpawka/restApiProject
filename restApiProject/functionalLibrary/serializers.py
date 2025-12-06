from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ["id", "name", "bio", "birth_date", "books"]

    def get_books(self, obj):
        qs = obj.book_set.all().order_by('title')
        return [
            {"id": b.id, "title": b.title, "publication_year": b.publication_year}
            for b in qs
        ]


class BookSerializer(serializers.ModelSerializer):
    # принимаем имя, возвращаем имя
    author = serializers.SlugRelatedField(
        queryset=Author.objects.all(),
        slug_field="name"
    )

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

    def validate(self, attrs):
        # создаём копию объекта: либо новый, либо обновляемый
        instance = Book(
            **attrs,
            id=getattr(self.instance, "id", None)   # важная строка!
        )

        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs
