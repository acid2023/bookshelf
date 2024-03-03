import lorem
import random
from functools import wraps
from typing import Callable


from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.db import OperationalError
from django.core.exceptions import ValidationError

from books.models import Book


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


def handle_db_erros(func: Callable) -> Callable | HttpResponseBadRequest:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Book.DoesNotExist:
            error_message = "Book not found"
            return HttpResponseBadRequest(error_message)
        except OperationalError:
            error_message = "Database not found or connection error"
            return HttpResponseServerError(error_message)
        except ValidationError:
            error_message = "values used for creating records are not valid"
            return HttpResponseBadRequest(error_message)
        except Exception as e:
            error_message = f"Error occurred in function '{func.__name__}': {str(e)}"
            return HttpResponseBadRequest(error_message)
    return wrapper
