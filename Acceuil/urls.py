from django.urls import path
from .views import page_accueil

urlpatterns = [
    path('', page_accueil, name='accueil'),
]
