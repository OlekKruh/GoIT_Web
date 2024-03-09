from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def hello_buratiny(request):
    return HttpResponse('<h1>Привет буратины!</h1>')
