import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import json
import requests
from bs4 import BeautifulSoup

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
    {
        'title': 'Scrape-quotes',
        'url_name': 'scrape_quotes',
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


def scrape_quotes_from_website(request):
    url = 'http://127.0.0.1:8000/'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('li')

        scraped_data = []

        for quote in quotes:
            author_name = quote.find('a').text
            paragraphs = quote.find_all('p')

            if paragraphs:
                quote_text = paragraphs[0].text
                tags = paragraphs[1].text.split(' | ')

                quote_data = {
                    'author': author_name,
                    'quote': quote_text,
                    'tags': tags,
                }

                scraped_data.append(quote_data)

        df = pd.DataFrame(scraped_data)

        excel_file = 'scraped_quotes.xlsx'
        df.to_excel(excel_file, index=False)

        with open(excel_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=scraped_quotes.xlsx'
        return HttpResponse(json.dumps(scraped_data), content_type='application/json')

    else:
        return HttpResponse(f"Failed to retrieve the page. Status code: {response.status_code}")
