from django.contrib import admin
from django.utils.html import format_html
from .models import PrestationMensuelle

class PrestationMensuelleAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'mois', 'annee',
        'total_avant_retenu', 'total_apres_retenu', 'net_a_payer',
        'voir_fiche'  # Bouton personnalisé
    )
    list_filter = ('mois', 'annee')
    readonly_fields = ('total_avant_retenu', 'total_apres_retenu', 'net_a_payer')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'poste', 'grade', 'fonction', 'mois', 'annee')
        }),
        ('Prestations', {
            'fields': (
                'consultations_urgences',
                'pharmacie_bonus',
                'prescriptions',
                'pensements',
                'pharmacie_nuit_weekend',
                'laboratoire_nuit_weekend',
                'aides_aux_actes',
                'prescriptions_laboratoire',
                'prescription_echo',
                'anesthesie',
            )
        }),
        ('Primes et retenues', {
            'fields': (
                'prime_caisse',
                'prime_transport',
                'anciennete',
                'prime_hospitalisation',  # Ajout ici
                'avance_salaire',
            )
        }),
        ('Totaux calculés', {
            'fields': (
                'total_avant_retenu',
                'total_apres_retenu',
                'net_a_payer',
            )
        }),
        ('Observation', {
            'fields': ('observation',)
        }),
    )

    def voir_fiche(self, obj):
        url = f"/Bulletin_paramedicaux/fiches/{obj.id}/"
        return format_html(
            '<a class="button" style="color: white; background-color: #2a9d8f; padding: 4px 8px; border-radius: 4px;" href="{}" target="_blank">Voir fiche</a>',
            url
        )
    voir_fiche.short_description = "Fiche utilisateur"

admin.site.register(PrestationMensuelle, PrestationMensuelleAdmin)
