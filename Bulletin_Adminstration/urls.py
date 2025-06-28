from django.urls import path
from .views import liste_fiches_paie

urlpatterns = [
    path('fiches/', liste_fiches_paie, name='liste_fiches_paie'),
]
