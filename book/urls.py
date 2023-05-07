from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('add-book/', BookCreateView.as_view(), name='add-book'),
    path('add-category/', add_category, name='add-category'),
    path('add-author/', add_author, name='add-author'),
    path('update-book/<int:pk>/', BookUpdateView.as_view(), name='update-book'),
    path('delete-book/<int:pk>/', BookDeleteView.as_view(), name='delete-book'),
    path(r'borrowed/', LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
    path('borrow/', BorrowCreateView.as_view(), name='borrow'),

]