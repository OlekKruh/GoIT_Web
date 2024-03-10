from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import json

# Create your views here.

menu = [
    {
        'title': 'About website',
        'url_name': 'about',
    },
    {
        'title': 'Quotes',
        'url_name': 'home'
    },
    {
        'title': 'Contact',
        'url_name': 'contact'
    },
    {
        'title': 'Login',
        'url_name': 'login'
    },
]

with open('json/authors_quotes.json', 'r', encoding='utf-8') as file:
    quote_db = json.load(file)

with open('json/authors_bio.json', 'r', encoding='utf-8') as file:
    bio_db = json.load(file)


def find_in_list_of_dicts(bio_db, full_name, author_name):
    for item in bio_db:
        if item.get(full_name) == author_name:
            return item
    return None


def quotes(request):
    data = {
        'title': 'Famous people quotes',
        'menu': menu,
        'posts': quote_db,
        'bio': bio_db,
    }
    return render(request, 'main/quotes.html', context=data)


def author_bio(request, author_name):
    author_bio = find_in_list_of_dicts(bio_db, 'Fullname', author_name)

    if not author_bio:
        return render(request, 'main/author_not_found.html', {'author_name': author_name, 'menu': menu})

    data = {
        'menu': menu,
        'author_bio': author_bio,
    }
    return render(request, 'main/authors_bio.html', context=data)


def about(request):
    return render(request, 'main/about.html', {'title': 'About website', 'menu': menu})


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Authorization")
