from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('post-detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add-book/', BookCreate.as_view() , name='add-book'),
    path('update-book/<int:pk>/', BookUpdate.as_view(), name='update-book'),
    path('delete-post/<int:pk>/', BookDelete.as_view(), name='delete-book'),
    path('author-detail/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('add-author/', AuthorCreate.as_view() , name='add-author'),
    path('update-author/<int:pk>/', AuthorUpdate.as_view(), name='update-author'),
    path('delete-author/<int:pk>/', AuthorDelete.as_view(), name='delete-author'),

]