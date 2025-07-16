from django.contrib import admin
from django.utils.html import format_html  # ← Import manquant
from .models import FichePrestation

class FichePrestationAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'mois', 'annee',
        'total_avant_retenu', 'total_apres_retenu',
        'net_a_payer', 'voir_fiche'  # ← ajout ici
    )
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

    def voir_fiche(self, obj):
        url = f"/Bulletin_Medecin/fiches/{obj.id}/"  
        return format_html(
            '<a class="button" style="color: white; background-color: #2a9d8f; padding: 4px 8px; border-radius: 4px;" href="{}" target="_blank">Voir fiche</a>',
            url
        )
    voir_fiche.short_description = "Fiche utilisateur"

admin.site.register(FichePrestation, FichePrestationAdmin)
