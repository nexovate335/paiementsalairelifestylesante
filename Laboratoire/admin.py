from django.contrib import admin
from .models import LaboTrios, LaboratoireMaison

@admin.register(LaboTrios)
class LaboTriosAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'tarif_maison', 'tarif_trios', 'benefice_maison',
        'msn_part_tarif_trios', 'total_g', 'msn_final', 'acteurs_total',
        'preleveur_nom', 'preleveur_montant', 'prescripteur_nom', 'prescripteur_montant'
    )
    readonly_fields = (
        'benefice_maison', 'msn_part_tarif_trios', 'total_g', 'msn_final', 'acteurs_total',
        'preleveur_montant', 'prescripteur_montant', 'created_at'
    )
    search_fields = ('libelle', 'preleveur_nom', 'prescripteur_nom')


from django.contrib import admin
from .models import LaboratoireMaison

@admin.register(LaboratoireMaison)
class LaboratoireMaisonAdmin(admin.ModelAdmin):
    list_display = (
        'libelle',
        'montant_total',
        'msn_part',
        'acteurs_part',

        'prescripteur_nom', 'prescripteur_gain',
        'technicien_nom', 'technicien_gain',
        'preleveur_nom', 'preleveur_gain',
        'assistante_nom', 'assistante_gain',

        'mois', 'annee',
    )

    list_filter = ('mois', 'annee')
    search_fields = ('libelle', 'prescripteur_nom', 'technicien_nom', 'preleveur_nom', 'assistante_nom')
    ordering = ['-annee', '-mois']


    