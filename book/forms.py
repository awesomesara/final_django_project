from django.forms import ModelForm
from django.utils.datetime_safe import datetime
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms



class BookForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Book
        fields = '__all__'


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email',]


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['slug', 'name']


class BorrowForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back', 'borrower', 'status']





