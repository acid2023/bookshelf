from django.contrib import admin
from books.views import create_books_handler, books_handler, book_handler, api_books_handler, api_book_handler
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_books/', create_books_handler),
    path('books/', books_handler),
    path('books/<int:book_id>/', book_handler),
    path('api/books/', api_books_handler),
    path('api/books/<int:book_id>/', api_book_handler),
]
