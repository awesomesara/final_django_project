import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=None)
    public_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='books', blank=True, null=True)


class CategoryModel(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)


class AuthorModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)