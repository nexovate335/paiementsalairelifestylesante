from django.contrib import admin
from .models import FichePrestation

@admin.register(FichePrestation)
class FichePrestationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'mois', 'annee', 'total_avant_retenu', 'total_apres_retenu', 'net_a_payer')
    search_fields = ('nom',)
    list_filter = ('mois', 'annee')
    readonly_fields = ('total_avant_retenu', 'total_apres_retenu', 'net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction', 'mois', 'annee')
        }),
        ('Prestations médicales', {
            'fields': (
                'consultations',
                'echographie_prescripteur',
                'echographie_acteur',
                'pourcentage_hospitalisation',
                'accouchements',
                'chirurgie',
                'aides',
                'prescription_labo',
                'bonus_pharmacie',
            )
        }),
        ('Primes et Retenues', {
            'fields': (
                'prime_transport',
                'anciennete',
                'avance_salaire',
            )
        }),
        ('Totaux', {
            'fields': (
                'total_avant_retenu',
                'total_apres_retenu',
                'net_a_payer',
            )
        }),
    )
