from django.contrib import admin
from .models import Accouchement

@admin.register(Accouchement)
class AccouchementAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'medecin', 'part_medecin',
        'sf', 'part_sf',
        'aide', 'part_aide',
        'pediatre', 'part_pediatre',
    )

    readonly_fields = (
        'maison',
        'part_medecin',
        'part_sf',
        'part_aide',
        'part_pediatre',
    )
