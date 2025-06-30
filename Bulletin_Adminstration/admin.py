from django.contrib import admin
from django.utils.html import format_html
from .models import FicheDePaie

@admin.register(FicheDePaie)
class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'mois', 'annee', 'affiche_net_a_payer', 'voir_fiche')
    search_fields = ('nom', 'poste', 'mois', 'annee')
    list_filter = ('mois', 'annee', 'poste')

    readonly_fields = (
        'affiche_total_avant_retenues',
        'affiche_total_retenues',
        'affiche_net_a_payer'
    )

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

    def voir_fiche(self, obj):
        url = f"/Bulletin_Adminstration/fiches/{obj.id}/"
        return format_html(
            '<a class="button" style="color: white; background-color: #2a9d8f; padding: 4px 8px; border-radius: 4px;" href="{}" target="_blank">Voir fiche</a>',
            url
        )
    voir_fiche.short_description = "Fiche utilisateur"
