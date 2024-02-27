from django.shortcuts import render
from books.models import Book
import lorem  # type: ignore

import random
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.defaultfilters import linebreaksbr
from functools import wraps
from typing import Callable


DB_FILEDS = [
    "title",
    "author_full_name",
    "year_of_publishing",
    "copies_printed",
    "short_description",
]


def get_lorem_name() -> str:
    name_1 = lorem.sentence().split()[0]
    name_2 = lorem.sentence().split()[0]
    name_3 = lorem.sentence().split()[0]
    return f"{name_1} {name_2} {name_3}"


def create_lorem_book() -> Book:
    title = lorem.sentence()
    author_full_name = get_lorem_name()
    year_of_publishing = random.randint(1900, 2022)
    copies_printed = random.randint(0, 100)
    short_description = lorem.paragraph()
    new_book = Book(title=title, author_full_name=author_full_name, year_of_publishing=year_of_publishing,
                    copies_printed=copies_printed, short_description=short_description)
    return new_book


def handle_db_erros(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    return wrapper


@handle_db_erros
def create_books_handler(request: HttpRequest) -> HttpResponse:
    for i in range(10):
        create_lorem_book().save()
    return HttpResponse("OK")


@handle_db_erros
def books_handler(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    if not books:
        return HttpResponseBadRequest("No books found - database is empty")
    columns = ['id'] + DB_FILEDS
    rows = []
    for book in books:
        row = []
        row.append(book.id)
        for field in columns[1:]:
            row.append(getattr(book, field))
        rows.append(row)
    context = {
        "columns": columns,
        "rows": rows
    }
    return render(request, "table.html", context)


@handle_db_erros
def book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.method == "GET":
        book = Book.objects.get(id=book_id)
        context = {"book": linebreaksbr(book)}  # type: ignore
        return render(request, "book.html", context)
    else:
        return HttpResponseBadRequest("Bad request")


@handle_db_erros
def api_books_handler(request: HttpRequest) -> JsonResponse | HttpResponse:
    books = Book.objects.all()
    if not books:
        return HttpResponseBadRequest("No books found - database is empty")
    books_data = []
    for book in books:
        books_data.append({
            "title": book.title,
            "author_full_name": book.author_full_name,
            "year_of_publishing": book.year_of_publishing,
            "copies_printed": book.copies_printed,
            "short_description": book.short_description
        })
    return JsonResponse(books_data, safe=False)


@handle_db_erros
def api_book_handler(request: HttpRequest, book_id: int) -> JsonResponse:
    book = Book.objects.get(id=book_id)
    return JsonResponse({
        "title": book.title,
        "author_full_name": book.author_full_name,
        "year_of_publishing": book.year_of_publishing,
        "copies_printed": book.copies_printed,
        "short_description": book.short_description
    })
