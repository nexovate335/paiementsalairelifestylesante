from django.contrib import admin
from .models import PaiementEchographie

@admin.register(PaiementEchographie)
class PaiementEchographieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant', 'created_at'
    )

    readonly_fields = (
        'msn_montant', 'acteur_montant', 'aide_montant', 'created_at'
    )

    fieldsets = (
        (None, {
            'fields': ('libelle', 'montant_total', 'acteur_nom', 'aide_nom')
        }),
        ('Montants calculés automatiquement', {
            'fields': ('msn_montant', 'acteur_montant', 'aide_montant', 'created_at')
        }),
    )
