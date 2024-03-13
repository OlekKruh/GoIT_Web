from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import LoginUserForm
from .forms import QuoteForm
from .models import Quote


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
            # Create a new Quote instance with the form data
            new_quote = Quote(
                quote_text=form.cleaned_data['quote_text'],
                author_name=form.cleaned_data['author_name'],
                tags=form.cleaned_data['tags']
            )
            # Save the new quote to the database
            new_quote.save()
            # Redirect to a success page or back to the form
            return redirect('add_quote_success')  # Replace 'add_quote_success' with the URL name of your success page
    else:
        form = QuoteForm()
    return render(request, 'main/add_quote.html', {'form': form})
