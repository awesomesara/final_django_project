from django.contrib import admin
from book.models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)