from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from books.models import *


class MainPageView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 4

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

