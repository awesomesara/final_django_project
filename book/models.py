import uuid
from django.db import models
from account.models import User
from datetime import date


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


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
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
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)

