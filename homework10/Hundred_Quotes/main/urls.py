from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotes, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('author_bio/<str:author_name>/', views.author_bio, name='author_bio'),
]
