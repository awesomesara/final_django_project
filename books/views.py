from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, View, CreateView, UpdateView
from .models import *


class MainPageView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 2

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['books'] = Book.objects.filter(Q(title__icontains=search)|
                                                       Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['books'] = Book.objects.filter(created__gte=start_date)
        else:
            context['books'] = Book.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = CategoryModel
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(category_id=self.slug)
        return context


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = AuthorModel
    template_name = 'author_create.html'
    fields = ['first_name', 'last_name', 'date_of_birth']
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = AuthorModel
    template_name = 'author_update.html'
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = AuthorModel
    template_name = 'author_delete.html'
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class BookDetailView(View):
    model = Book
    template_name = 'book-detail.html'
    context_object_name = 'book'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'book_create.html'
    fields = ['title', 'author', 'category', 'price', 'image']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'book_update.html'
    fields = ['title', 'author', 'category', 'price', 'image']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


class AuthorDetailView(DetailView):
    model = AuthorModel
    template_name = 'author-detail.html'
    context_object_name = 'author'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author_id=self.slug)
        return context

