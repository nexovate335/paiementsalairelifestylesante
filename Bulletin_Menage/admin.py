from django.contrib import admin
from django.utils.html import format_html
from .models import FicheDePaie

class FicheDePaieAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'poste', 'grade', 'fonction',
        'mois', 'annee',
        'total_avant_retenues', 'total_retenues', 'net_a_payer',
        'voir_fiche',  # ajouté ici
    )
    readonly_fields = (
        'total_avant_retenues',
        'total_retenues',
        'net_a_payer'
    )
    search_fields = ('nom', 'poste', 'grade', 'fonction')
    list_filter = ('mois', 'annee')

    def voir_fiche(self, obj):
        url = f"/Bulletin_Adminstration/fiches/{obj.id}/"
        return format_html(
            '<a class="button" style="color: white; background-color: #2a9d8f; padding: 4px 8px; border-radius: 4px;" href="{}" target="_blank">Voir fiche</a>',
            url
        )
    voir_fiche.short_description = "Fiche utilisateur"

admin.site.register(FicheDePaie, FicheDePaieAdmin)
