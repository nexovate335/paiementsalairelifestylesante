from django.contrib import admin
from .models import ActeMedical, PaiementMonitorage

class ActeMedicalAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'libelle', 'montant_total',
        'msn_montant', 'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant', 'created_at'
    )
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


@admin.register(PaiementMonitorage)
class PaiementMonitorageAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_nom', 'msn_montant', 'acteur_nom', 'acteur_montant', 'created_at')
    list_filter = ('created_at',)
