from django.contrib import admin
from .models import Consultation, CertificatMedical 
    
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'type', 'montant_total','mois','annee',
        'msn_montant', 'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant', 'created_at',
    )
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


@admin.register(CertificatMedical)
class CertificatMedicalAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total','mois','annee',
        'msn_nom', 'msn_montant',
        'acteur_nom', 'acteur_montant',
        'created_at'
    )
    readonly_fields = ('msn_montant', 'acteur_montant', 'created_at')

    def save_model(self, request, obj, form, change):
        # Calculer la répartition AVANT la sauvegarde
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


