from django.contrib import admin
from .models import PrestationMensuelle

@admin.register(PrestationMensuelle)
class PrestationMensuelleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'mois', 'annee', 'total_avant_retenu', 'total_apres_retenu', 'net_a_payer')
    search_fields = ('nom',)
    list_filter = ('mois', 'annee')
    readonly_fields = ('total_avant_retenu', 'total_apres_retenu', 'net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction', 'mois', 'annee')
        }),
        ('Prestations', {
            'fields': (
                'Accouchement',
                'actes',
                'prescriptions_laboratoire',
                'prime_hospitalisation',
                'prime_transport',
                'anciennete',
            )
        }),
        ('Retenue', {
            'fields': ('avance_salaire',)
        }),
        ('Totaux calculés', {
            'fields': ('total_avant_retenu', 'total_apres_retenu', 'net_a_payer')
        }),
        ('Observation', {
            'fields': ('observation',)
        }),
    )
