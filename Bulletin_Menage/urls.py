from django.urls import path
from .views import fiche_detail

urlpatterns = [
    path('fiches/<int:id>/', fiche_detail, name='fiche_detail'),
]
