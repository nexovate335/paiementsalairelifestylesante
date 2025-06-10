from django.contrib import admin
from .models import LaboTrios

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
