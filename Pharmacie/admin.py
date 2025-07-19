from django.contrib import admin
from .models import Pharmacie

@admin.register(Pharmacie)
class PharmacieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 
        'prix_vente',
        'mois',
        'annee', 
        'benefice', 
        'maison', 
        'controleur', 
        'vendeur', 
        'prescripteur',
    )

    readonly_fields = (
        'benefice',
        'maison',
        'controleur',
        'vendeur',
        'prescripteur',
    )
