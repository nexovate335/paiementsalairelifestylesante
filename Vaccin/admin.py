from django.contrib import admin
from .models import Vaccin

class VaccinAdmin(admin.ModelAdmin):
    list_display = (
        'libelle',
        'montantTT',
        'maison',
        'nom_acteur1', 'acteur1_part',
        'nom_acteur2', 'acteur2_part',
        'nom_acteur3', 'acteur3_part',
    )

    readonly_fields = (
        'maison',
        'acteur1_part',
        'acteur2_part',
        'acteur3_part',
    )
