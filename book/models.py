from django.db import models
import uuid
from account.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author)
    description = models.TextField(blank=True, null=True, default='It is a new book')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    def __str__(self) -> str:
        return self.title


class Exemplar(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    print_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{Book.objects.get(id=self.book.id).title} - {self.code}"


class Borrower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


def get_time():
    return datetime.now() + timedelta(seconds=15)


class Borrow(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    exemplar = models.ForeignKey('Exemplar', on_delete=models.CASCADE)
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    start = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True, default=get_time)

    def __str__(self):
        instance = Exemplar.objects.get(id=self.exemplar.id)
        borrower = Borrower.objects.get(id=self.borrower.id)

        return f"{borrower.user.first_name} {borrower.user.last_name} - {instance}"

    def calculate_fine(self):
        delta = (timezone.now() - self.end).seconds

        if self.status and delta > 0:
            self.borrower.debt = delta
            self.borrower.save()