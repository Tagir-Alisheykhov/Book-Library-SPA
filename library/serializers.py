from rest_framework import serializers

from .models import Author, Book, BookIssue
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов"""

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книг"""

    authors = AuthorSerializer(many=True, read_only=True)
    authors_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        write_only=True,
        source='authors'
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'authors', 'authors_ids', 'isbn',
            'publication_date', 'pages', 'genre',
            'total_quantity', 'available_quantity', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'available_quantity']


class BookIssueSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи книг"""

    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BookIssue
        fields = [
            'id', 'book', 'user', 'issued_at', 'returned_at',
            'status', 'book_title', 'user_username'
        ]
        read_only_fields = ['id', 'issued_at', 'returned_at']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей (без пароля)"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
