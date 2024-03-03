from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.defaultfilters import linebreaksbr
from django.forms.models import model_to_dict

from books.models import Book
from books.utils import create_lorem_book, handle_db_erros


@handle_db_erros
def create_books_handler(request: HttpRequest) -> HttpResponse:
    for _ in range(10):
        create_lorem_book().save()
    return HttpResponse("OK")


@handle_db_erros
def books_handler(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    if not books:
        return HttpResponseBadRequest("No books found - database is empty")
    columns = model_to_dict(books[0]).keys()
    rows = [model_to_dict(book).values() for book in books]
    context = {"columns": columns, "rows": rows}
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
