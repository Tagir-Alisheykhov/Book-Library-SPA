from django.contrib import admin
from .models import Author, Book, BookIssue


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админка для авторов"""

    list_display = ['id', 'first_name', 'last_name', 'birth_date', 'created_at']
    list_filter = ['created_at', 'birth_date']
    search_fields = ['first_name', 'last_name']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админка для книг"""

    list_display = [
        'id', 'title', 'isbn', 'genre',
        'total_quantity', 'available_quantity',
        'publication_date', 'created_at'
    ]
    list_filter = ['genre', 'publication_date', 'created_at']
    search_fields = ['title', 'isbn', 'authors__first_name', 'authors__last_name']
    ordering = ['title']
    readonly_fields = ['created_at']
    filter_horizontal = ['authors']  # Интерфейс для выбора авторов

    def get_authors(self, obj):
        """Добавляем отображение авторов в списке"""
        return ", ".join([f"{author.first_name} {author.last_name}"
                         for author in obj.authors.all()])
    get_authors.short_description = 'Authors'


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    """Админка для выдачи книг"""

    list_display = [
        'id', 'book', 'user', 'issued_at',
        'returned_at', 'status'
    ]
    list_filter = ['status', 'issued_at', 'returned_at']
    search_fields = [
        'book__title', 'user__username',
        'user__first_name', 'user__last_name'
    ]
    ordering = ['-issued_at']
    readonly_fields = ['issued_at']
    # Фильтр по статусу в списке
    list_filter = ['status', 'issued_at', 'returned_at', 'book__genre']
    # Добавляем удобные фильтры
    date_hierarchy = 'issued_at'
    # Группировка полей
    fieldsets = (
        ('Основная информация', {
            'fields': ('book', 'user', 'status')
        }),
        ('Даты', {
            'fields': ('issued_at', 'returned_at'),
            'classes': ('collapse',)
        }),
    )
