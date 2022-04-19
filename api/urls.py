from django.urls import path
from django.conf.urls import include
from api.views import search_view

urlpatterns = [
    path('search/', search_view, name='search' ),
]