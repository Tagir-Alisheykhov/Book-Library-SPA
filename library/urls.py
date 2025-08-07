"""
Конечные точки приложения `library`.
"""

from django.urls import path

from library.apps import LibraryConfig
from . import views


app_name = LibraryConfig.name
urlpatterns = [
    # Авторы
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),

    # Книги
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Выдача книг
    path('book-issues/', views.BookIssueListCreateView.as_view(), name='book-issue-list-create'),
    path('book-issues/<int:pk>/', views.BookIssueDetailView.as_view(), name='book-issue-detail'),
]
