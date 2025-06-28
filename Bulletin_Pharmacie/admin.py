from django.contrib import admin
from .models import FicheDePaie

@admin.register(FicheDePaie)
class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'mois', 'annee', 'total_avant_retenues', 'total_retenues', 'net_a_payer')
    search_fields = ('nom',)
    list_filter = ('mois', 'annee')
    readonly_fields = ('total_avant_retenues', 'total_retenues', 'net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction', 'mois', 'annee')
        }),
        ('Prestations', {
            'fields': (
                'pourcentage_prestations',
                'prime_transport',
                'anciennete',
            )
        }),
        ('Retenue', {
            'fields': ('avance_salaire',)
        }),
        ('Totaux calculés', {
            'fields': ('total_avant_retenues', 'total_retenues', 'net_a_payer')
        }),
    )
