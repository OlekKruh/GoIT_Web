from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import LoginUserForm
from .forms import QuoteForm
import json


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Extract the form data
            quote_text = form.cleaned_data['quote_text']
            author_name = form.cleaned_data['author_name']
            tags = form.cleaned_data['tags']

            # Create a dictionary for the new quote
            new_quote = {
                'quote_text': quote_text,
                'author_name': author_name,
                'tags': tags
            }

            with open('json/authors_quotes.json', 'w', encoding='utf-8') as file:
                data = json.load(file)
                data.append(new_quote)
                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)

            return redirect('add_quote_success')
    else:
        form = QuoteForm()
    return render(request, 'main/add_quote.html', {'form': form})