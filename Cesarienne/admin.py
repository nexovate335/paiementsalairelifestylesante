from django.contrib import admin
from .models import Cesarienne

@admin.register(Cesarienne)
class CesarienneAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'chirurgien', 'part_chirurgien',
        'aide', 'part_aide',
        'anesthesiste', 'part_anesthesiste',
        'panseur', 'part_panseur',
        'instrumentiste', 'part_instrumentiste',
        'pediatre', 'part_pediatre',
        'sf', 'part_sf',
    )

    readonly_fields = (
        'maison',
        'part_chirurgien',
        'part_aide',
        'part_anesthesiste',
        'part_panseur',
        'part_instrumentiste',
        'part_pediatre',
        'part_sf',
    )
