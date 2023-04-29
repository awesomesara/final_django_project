from django import forms
from django.forms import ModelForm
from .models import *


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