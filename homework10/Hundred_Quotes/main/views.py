from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
import requests
from bs4 import BeautifulSoup

from users.forms import QuoteForm

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
    {
        'title': 'Add_quotes',
        'url_name': 'add_quote',
    },
]


def find_in_list_of_dicts(bio_db, full_name, author_name):
    for item in bio_db:
        if item.get(full_name) == author_name:
            return item
    return None


def quotes(request):
    try:
        with open('json/authors_quotes.json', 'r', encoding='utf-8') as file:
            quote_db = json.load(file)
    except FileNotFoundError:
        quote_db = []

    data = {
        'title': 'Famous people quotes',
        'menu': menu,
        'posts': quote_db,
    }

    return render(request, 'main/quotes.html', context=data)


def author_bio(request, author_name):
    try:
        with open('json/authors_bio.json', 'r', encoding='utf-8') as file:
            bio_db = json.load(file)
    except FileNotFoundError:
        bio_db = []

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
    return render(request, 'main/about.html', {'title': 'Contact', 'menu': menu})


def login(request):
    return render(request, 'D:/MyProjects/GoIT_Web/homework10/Hundred_Quotes/users/templates/users/login.html',
                  {'title': 'Contact', 'menu': menu})


def scrape_quotes_from_website(request):
    url = 'https://quotes.toscrape.com'
    dict_of_quotes = []
    dict_of_authors_bio = []
    counter = 1

    while url:
        my_requests = requests.get(url)
        src = my_requests.text
        soup = BeautifulSoup(src, 'lxml')

        quotes = soup.find_all(class_='quote')
        for quote in quotes:
            text = quote.find('span').text
            author = quote.find('small').text
            tags = [tag.text for tag in quote.find_all(class_='tag')]
            dict_of_quotes.append(
                {
                    'Author': author,
                    'Quote': text,
                    'Tags': tags,
                }
            )

            author_bio_link = 'https://quotes.toscrape.com' + quote.find('a')['href']
            my_author_bio_requests = requests.get(author_bio_link)
            src_author = my_author_bio_requests.text
            author_soup = BeautifulSoup(src_author, 'lxml')

            fullname = author_soup.find(class_='author-title').text
            born_date = author_soup.find(class_='author-born-date').text
            born_location = author_soup.find(class_='author-born-location').text
            description = author_soup.find(class_='author-description').text.strip()
            dict_of_authors_bio.append(
                {
                    'Fullname': fullname,
                    'Born_Date': born_date,
                    'Born_Location': born_location,
                    'Description': description,
                }
            )

        next_page_href = soup.find(class_='next')
        if next_page_href:
            next_page_link = 'https://quotes.toscrape.com' + next_page_href.find('a')['href']
            url = next_page_link
        else:
            break

    with open('json/authors_quotes.json', 'w', encoding='utf-8') as file:
        json.dump(dict_of_quotes, file, indent=4, ensure_ascii=False)

    with open('json/authors_bio.json', 'w', encoding='utf-8') as file:
        json.dump(dict_of_authors_bio, file, indent=4, ensure_ascii=False)

    return render(request, 'main/about.html', {'title': 'Scrape Complit', 'menu': menu})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the form data to the database
            return redirect('home')  # Replace 'home' with the name of your home page URL pattern
    else:
        form = QuoteForm()
    return render(request, 'main/add_quote.html', {'title': 'Famous people quotes', 'menu': menu, 'form': form})
