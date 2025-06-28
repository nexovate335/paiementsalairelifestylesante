from django.contrib import admin
from .models import FicheDePaie

@admin.register(FicheDePaie)
class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'mois', 'annee', 'net_a_payer')
    search_fields = ('nom', 'poste', 'mois', 'annee')
    readonly_fields = ('total_avant_retenues', 'total_retenues', 'net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction', 'mois', 'annee')
        }),
        ('Prestations', {
            'fields': (
                'prestations',
                'transport_jour',
                'transport_nuit_feries',
                'autres_prestations',
                'prime_anciennete',
            )
        }),
        ('Retenues', {
            'fields': ('avance_salaire',)
        }),
        ('Totaux calculés', {
            'fields': (
                'total_avant_retenues',
                'total_retenues',
                'net_a_payer'
            )
        }),
    )
