from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('home', index, name="index"),
    path('scrape', scrape, name="scrape"),
    path('show_profiles', profiles, name="show_profiles")
    ]
