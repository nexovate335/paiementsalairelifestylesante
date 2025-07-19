from django.contrib import admin
from .models import Pansement

class PansementAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montantTT','mois','annee','type_maison', 'montant_maison', 'acteur', 'montant_acteur')
    readonly_fields = ('montant_maison', 'type_maison', 'montant_acteur')

    fieldsets = (
        (None, {
            'fields': ('libelle', 'montantTT','mois','annee')
        }),
        ('Acteur', {
            'fields': ('acteur', 'montant_acteur')
        }),
        ('Montant Maison (auto-calculé)', {
            'fields': ('montant_maison', 'type_maison'),
        }),
    )

admin.site.register(Pansement, PansementAdmin)
