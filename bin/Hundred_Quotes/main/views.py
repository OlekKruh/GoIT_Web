from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Quote, AuthorBio
from django.core.exceptions import ObjectDoesNotExist

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
        'url_name': 'users:login'
    },
    {
        'title': 'Scrape-quotes',
        'url_name': 'scrape_quotes',
    },
    # {
    #     'title': 'Add_quotes',
    #     'url_name': 'add_quote',
    # },
]


def find_in_list_of_dicts(bio_db, full_name, author_name):
    for item in bio_db:
        if item.get(full_name) == author_name:
            return item
    return None


def quotes(request):
    quotes = Quote.objects.all()
    data = {
        'title': 'Famous people quotes',
        'menu': menu,
        'posts': quotes,
    }
    return render(request, 'main/quotes.html', context=data)


def author_bio(request, author_name):
    try:
        author_bio = AuthorBio.objects.get(fullname=author_name)
    except ObjectDoesNotExist:
        return render(request, 'main/author_not_found.html', {'author_name': author_name, 'menu': menu})

    data = {
        'menu': menu,
        'author_bio': author_bio,
    }
    return render(request, 'main/authors_bio.html', context=data)


def about(request):
    return render(request, 'main/about.html', {'title': 'About website', 'menu': menu})


def contact(request):
    return render(request, 'main/about.html', {'title': 'Contact', 'menu': menu})


def login(request):
    return render(request, 'D:/MyProjects/GoIT_Web/homework10/Hundred_Quotes/users/templates/users/login.html',
                  {'title': 'Contact', 'menu': menu})


def scrape_quotes_from_website(request):
    url = 'https://quotes.toscrape.com'

    while url:
        my_requests = requests.get(url)
        src = my_requests.text
        soup = BeautifulSoup(src, 'lxml')

        quotes = soup.find_all(class_='quote')
        for quote in quotes:
            text = quote.find('span').text
            author = quote.find('small').text
            tags = [tag.text for tag in quote.find_all(class_='tag')]

            q = Quote.objects.create(author_name=author, quote_text=text, tags=tags)

            author_bio_link = 'https://quotes.toscrape.com' + quote.find('a')['href']
            my_author_bio_requests = requests.get(author_bio_link)
            src_author = my_author_bio_requests.text
            author_soup = BeautifulSoup(src_author, 'lxml')

            fullname = author_soup.find(class_='author-title').text
            born_date_str = author_soup.find(class_='author-born-date').text
            # Convert the date string to the correct format
            from datetime import datetime
            born_date = datetime.strptime(born_date_str, '%B %d, %Y').strftime('%Y-%m-%d')
            born_location = author_soup.find(class_='author-born-location').text
            description = author_soup.find(class_='author-description').text.strip()

            AuthorBio.objects.create(fullname=fullname, born_date=born_date, born_location=born_location,
                                     description=description, quote=q)

        next_page_href = soup.find(class_='next')
        if next_page_href:
            next_page_link = 'https://quotes.toscrape.com' + next_page_href.find('a')['href']
            url = next_page_link
        else:
            break

    return render(request, 'main/about.html', {'title': 'Scrape Complete', 'menu': menu})