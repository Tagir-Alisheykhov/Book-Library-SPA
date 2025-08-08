from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Author, Book, BookIssue
from .serializers import AuthorSerializer, BookSerializer, BookIssueSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    get:
    Получить список всех авторов
    post:
    Создать нового автора (только для админов)
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]  # Только админы/персонал
        return [IsAuthenticated()]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Получить информацию об авторе по ID
    put:
    Полное обновление информации об авторе по ID
    patch:
    Обновить отдельные поля автора по ID
    delete:
    Удалить информацию об авторе по ID
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BookListCreateView(generics.ListCreateAPIView):
    """
    get:
    Получить список всех книг с фильтрацией
    Фильтры:
    - ?title=название - поиск по названию
    - ?author=фамилия - поиск по автору
    - ?genre=жанр - поиск по жанру
    - ?available=true/false - только доступные/недоступные книги
    post:
    Создать новую книгу (только для админов)
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """Фильтрация книг по параметрам"""
        queryset = Book.objects.all()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        genre = self.request.query_params.get('genre', None)
        available = self.request.query_params.get('available', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(authors__last_name__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if available and available.lower() == 'true':
            queryset = queryset.filter(available_quantity__gt=0)
        elif available and available.lower() == 'false':
            queryset = queryset.filter(available_quantity=0)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """При создании книги available_quantity = total_quantity"""
        total = serializer.validated_data.get('total_quantity', 1)
        serializer.save(available_quantity=total)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Получить детальную информацию о книге по ID
    put:
    Полное обновление информации о книге по ID
    patch:
    Обновить отдельные поля книги по ID
    delete:
    Удалить информацию об авторе по ID
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BookIssueListCreateView(generics.ListCreateAPIView):
    """
    get:
    Получить список выдач книг
    Для обычных пользователей - только свои выдачи
    Для админов - все выдачи
    post:
    Создать но
    serializer_class = BookIssueSerializer
    """
    serializer_class = BookIssueSerializer

    def get_queryset(self):
        """Пользователи видят только свои выдачи, админы - все"""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return BookIssue.objects.all()
            return BookIssue.objects.filter(user=self.request.user)
        return BookIssue.objects.none()

    def get_permissions(self):
        """Только персонал может выдавать книги"""
        if self.request.method == 'POST':
            return [IsAdminUser()]  # Только админы/персонал
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Логика выдачи книги (только персонал)"""
        book = serializer.validated_data['book']
        if book.available_quantity <= 0:
            raise serializers.ValidationError("Нет доступных экземпляров книги")

        # Атомарная операция: уменьшает количество и создает запись
        with transaction.atomic():
            book.available_quantity -= 1
            book.save()
            serializer.save(status='issued')


class BookIssueDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Получить детальную информацию о выдаче книги по ID
    put:
    Полное обновление информации о выдаче книги по ID
    patch:
    Обновить отдельные поля о выдаче книги по ID
    """

    serializer_class = BookIssueSerializer

    def get_queryset(self):
        """Пользователи видят только свои выдачи, админы - все"""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return BookIssue.objects.all()
            return BookIssue.objects.filter(user=self.request.user)
        return BookIssue.objects.none()

    def update(self, request, *args, **kwargs):
        """Логика возврата книги"""
        instance = self.get_object()

        # Проверяет, что книга еще не возвращена
        if instance.status == 'returned':
            return Response(
                {"detail": "Книга уже возвращена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Атомарная операция: увеличивает количество и обновляет запись
        with transaction.atomic():
            instance.book.available_quantity += 1
            instance.book.save()
            instance.returned_at = timezone.now()
            instance.status = 'returned'
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
