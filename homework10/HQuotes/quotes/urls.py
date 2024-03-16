from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('quotes/', views.quotes_view, name='quotes'),
    path('login/', LoginView.as_view(template_name='quotes/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('start-scraping/', views.start_scraping, name='start_scraping'),
    path('clear-quotes/', views.clear_quotes, name='clear_quotes'),
    path('author/<str:author_name>/', views.author_detail, name='author_detail'),
]