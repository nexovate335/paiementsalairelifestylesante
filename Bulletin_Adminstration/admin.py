from django.contrib import admin
from .models import FicheDePaie

@admin.register(FicheDePaie)
class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'mois', 'annee', 'affiche_net_a_payer')
    search_fields = ('nom', 'poste', 'mois', 'annee')
    list_filter = ('mois', 'annee', 'poste')

    readonly_fields = ('affiche_total_avant_retenues', 'affiche_total_retenues', 'affiche_net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction')
        }),
        ('Période de paie', {
            'fields': ('mois', 'annee')
        }),
        ('Prestations', {
            'fields': (
                'pourcentage_prestations',
                'bonus_prestations',
                'transport_reunion',
                'prime_informatique',
                'prime_responsabilite',
                'prime_transport',
                'anciennete',
            )
        }),
        ('Retenues', {
            'fields': ('avance_salaire',)
        }),
        ('Totaux', {
            'fields': (
                'affiche_total_avant_retenues',
                'affiche_total_retenues',
                'affiche_net_a_payer'
            )
        }),
    )

    def affiche_total_avant_retenues(self, obj):
        return obj.total_avant_retenues()
    affiche_total_avant_retenues.short_description = "Total avant retenues"

    def affiche_total_retenues(self, obj):
        return obj.total_retenues()
    affiche_total_retenues.short_description = "Total retenues"

    def affiche_net_a_payer(self, obj):
        return obj.net_a_payer()
    affiche_net_a_payer.short_description = "Net à payer"
