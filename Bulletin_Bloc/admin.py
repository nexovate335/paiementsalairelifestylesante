from django.contrib import admin
from .models import FicheDePaie

@admin.register(FicheDePaie)
class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'poste', 'grade', 'fonction',
        'mois', 'annee',
        'total_avant_retenues', 'total_retenues', 'net_a_payer'
    )
    readonly_fields = (
        'total_avant_retenues',
        'total_retenues',
        'net_a_payer',
    )
    search_fields = ('nom', 'poste', 'grade', 'fonction')
    list_filter = ('mois', 'annee')
