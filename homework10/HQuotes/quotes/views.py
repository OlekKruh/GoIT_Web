from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import QuoteForm
from .models import Quote, Author
import requests
from bs4 import BeautifulSoup


def home(request):
    return render(request, 'quotes/home.html')


def about(request):
    return render(request, 'quotes/about.html')


def login(request):
    return render(request, 'quotes/login.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes')
    else:
        form = UserCreationForm()
    return render(request, 'quotes/register.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            author, created = Author.objects.get_or_create(fullname=author_name)

            quote = Quote(
                text=form.cleaned_data['text'],
                author=author,
                tags=form.cleaned_data['tags']
            )
            quote.save()

            return redirect('quotes')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})


def quotes_view(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quotes.html', {'quotes': quotes})


def scrape_quotes_from_website(request):
    url = 'https://quotes.toscrape.com'
    quotes_saved = 0

    while url:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all(class_='quote')
        for quote in quotes:
            text = quote.find('span').text
            author_name = quote.find('small').text
            tags = ', '.join(tag.text for tag in quote.find_all(class_='tag'))

            author, created = Author.objects.get_or_create(fullname=author_name)
            if created:
                author_bio_link = 'https://quotes.toscrape.com' + quote.find('a')['href']
                bio_response = requests.get(author_bio_link)
                author_soup = BeautifulSoup(bio_response.text, 'lxml')

                born_date_str = author_soup.find(class_='author-born-date').text
                born_date = datetime.strptime(born_date_str, '%B %d, %Y')
                born_location = author_soup.find(class_='author-born-location').text.replace('in ', '', 1)  # Удаляем префикс "in "
                description = author_soup.find(class_='author-description').text.strip()

                author.born_date = born_date
                author.born_location = born_location
                author.description = description
                author.save()

            _, created = Quote.objects.get_or_create(
                text=text,
                author=author,
                defaults={'tags': tags}
            )
            if created:
                quotes_saved += 1

        next_page = soup.find(class_='next')
        url = 'https://quotes.toscrape.com' + next_page.find('a')['href'] if next_page else None

    return HttpResponse(f"Scraping completed. {quotes_saved} quotes were saved.")


@login_required
def start_scraping(request):
    scrape_quotes_from_website(request)
    return HttpResponseRedirect(reverse('quotes'))


@login_required
def clear_quotes(request):
    Quote.objects.all().delete()
    return HttpResponseRedirect(reverse('quotes'))


def author_detail(request, author_name):
    try:
        author_bio = Author.objects.get(fullname=author_name)
    except ObjectDoesNotExist:
        return render(request, 'quotes/author_not_found.html', {'author_name': author_name})

    return render(request, 'quotes/author_detail.html', {'author_bio': author_bio})
