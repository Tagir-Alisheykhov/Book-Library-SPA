from django.db import models
from django.conf import settings


class Author(models.Model):
    """Модель автора книги"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """Модель книги в библиотеке"""

    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    pages = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (доступно: {self.available_quantity}/{self.total_quantity})"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class BookIssue(models.Model):
    """Модель выдачи книги пользователю"""

    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')

    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"

    class Meta:
        verbose_name = "Book Issue"
        verbose_name_plural = "Book Issues"
