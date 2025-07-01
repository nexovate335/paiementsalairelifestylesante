from django.contrib import admin
from django.utils.html import format_html
from .models import FicheDePaie

class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'mois', 'annee',
        'total_avant_retenues', 'total_retenues', 'net_a_payer',
        'voir_fiche',  # Ajouté ici pour afficher le bouton
    )
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

    def voir_fiche(self, obj):
        url = f"/Bulletin_Pharmacie/fiches/{obj.id}/"
        return format_html(
            '<a class="button" style="color: white; background-color: #2a9d8f; padding: 4px 8px; border-radius: 4px;" href="{}" target="_blank">Voir fiche</a>',
            url
        )
    voir_fiche.short_description = "Fiche utilisateur"

admin.site.register(FicheDePaie, FicheDePaieAdmin)
