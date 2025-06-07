from django.contrib import admin
from .models import ActeORL

@admin.register(ActeORL)
class ActeORLAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_tt', 'montant_msn', 'montant_acteur')
    search_fields = ('libelle',)
    list_filter = ('libelle',)
    readonly_fields = ('montant_msn', 'montant_acteur')  # Pour éviter la modification manuelle

    fieldsets = (
        (None, {
            'fields': ('libelle', 'montant_tt')
        }),
        ('Montants calculés', {
            'fields': ('montant_msn', 'montant_acteur'),
            'classes': ('collapse',)
        }),
    )
