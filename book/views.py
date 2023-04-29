from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import AuthorForm, CategoryForm
from .models import Book, Exemplar, Borrower, Borrow, Category
from django.utils import timezone


class CategoryDetailView(DetailView):
    model = Category
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


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'add_category.html', context)


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
            context['books'] = Book.objects.filter(Q(title__icontains=search) |
                                                       Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['books'] = Book.objects.filter(created__gte=start_date)
        else:
            context['books'] = Book.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book-detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['instances'] = len(Exemplar.objects.filter(book=context['book'].id))

        return context


class BookCreateView(CreateView):
    model = Book
    template_name = 'add-book.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'update-book.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('book-detail', kwargs={"pk": pk})


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'delete-book.html'
    success_url = reverse_lazy('home')
    success_message = 'Successfully deleted!'


@login_required
def add_author(request):
    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'add_authors.html', context)

@login_required
def add_author(request):
    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'add_authors.html', context)


class BorrowCreateView(CreateView):
    model = Borrow
    fields = ['borrower']
    success_url = reverse_lazy('home')
    template_name = 'crud/create.html'

    def form_valid(self, form):
        last_borrow = Borrow.objects.filter(borrower=form.instance.borrower).last()

        if form.instance.borrower.debt:
            form.add_error('borrower', 'The user has\'t paid the fine')

            return self.form_invalid(form)

        if last_borrow is not None and timezone.now() < last_borrow.end:
            form.add_error('borrower', 'The user has already borrowed a book')

            return self.form_invalid(form)

        exemplar = Exemplar.objects.get(id=self.kwargs['exemplar'])
        exemplar.status = 0
        exemplar.save()

        form.instance.exemplar = exemplar

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('exemplar-detail', kwargs={'pk': self.object.exemplar.id})