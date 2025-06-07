from django.contrib import admin
from .models import (
    PaiementSimple,
    PaiementIVA_IVL,
    HVV,
    ActeMedical,
    ActeMedicalSimple,
    ActeMedicalIntermediaire
)

@admin.register(PaiementSimple)
class PaiementSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'type_paiement', 'libelle', 'montant_total', 
        'msn_nom', 'msn_montant', 
        'acteur_nom', 'acteur_montant',
        'created_at'
    )
    search_fields = ('libelle', 'acteur_nom')
    list_filter = ('type_paiement', 'created_at')

@admin.register(PaiementIVA_IVL)
class PaiementIVA_IVLAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 
        'msn_montant',
        'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant',
        'created_at'
    )
    search_fields = ('libelle', 'acteur_nom', 'aide_nom')
    list_filter = ('created_at',)

@admin.register(HVV)
class HVVAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total',
        'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'repartition_detaillee',
        'created_at'
    )
    search_fields = ('libelle', 'chirurgien_nom')
    list_filter = ('created_at',)
    readonly_fields = ('repartition_detaillee',)

@admin.register(ActeMedical)
class ActeMedicalAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total',
        'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at'
    )
    search_fields = ('libelle', 'chirurgien_nom')
    list_filter = ('type_acte', 'created_at')

@admin.register(ActeMedicalSimple)
class ActeMedicalSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total',
        'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
        'repartition_detaillee',
        'created_at'
    )
    search_fields = ('libelle', 'chirurgien_nom')
    list_filter = ('type_acte', 'created_at')
    readonly_fields = ('repartition_detaillee',)

@admin.register(ActeMedicalIntermediaire)
class ActeMedicalIntermediaireAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total',
        'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'aide_nom', 'aide_montant',
        'repartition_detaillee',
        'created_at'
    )
    search_fields = ('libelle', 'chirurgien_nom')
    list_filter = ('type_acte', 'created_at')
    readonly_fields = ('repartition_detaillee',)
