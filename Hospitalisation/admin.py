from django.contrib import admin
from .models import (
    PaiementHospitalisation,
    PaiementIVA_IVL,
    PaiementMonitorage,
    HVV,
    ActeMedical,
    ActeMedicalSimple,
    ActeMedicalIntermediaire,
    ActeurHospitalisation

)

from django.contrib import admin
from .models import PaiementHospitalisation, ActeurHospitalisation

class ActeurHospitalisationInline(admin.TabularInline):
    model = ActeurHospitalisation
    extra = 1

@admin.register(PaiementHospitalisation)
class PaiementHospitalisationAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_nom', 'msn_montant', 'repartition_detaillee', 'created_at')
    inlines = [ActeurHospitalisationInline]
    readonly_fields = ('msn_montant', 'repartition_detaillee', 'created_at')

    def save_model(self, request, obj, form, change):
        # Enregistre d'abord le paiement
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Enregistre les acteurs liés
        super().save_related(request, form, formsets, change)
        # Une fois que tout est enregistré, appelle la répartition
        form.instance.calcul_repartition()
        form.instance.save()


@admin.register(PaiementIVA_IVL)
class PaiementIVA_IVLAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_montant', 'acteur_nom', 'acteur_montant', 'aide_nom', 'aide_montant', 'created_at')
    search_fields = ('libelle', 'acteur_nom', 'aide_nom')
    list_filter = ('created_at',)


@admin.register(PaiementMonitorage)
class PaiementMonitorageAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_nom', 'msn_montant', 'acteur_nom', 'acteur_montant', 'created_at')
    search_fields = ('libelle', 'msn_nom', 'acteur_nom')
    list_filter = ('created_at',)


@admin.register(HVV)
class HVVAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
        'repartition_detaillee',
    )
    search_fields = ('libelle', 'chirurgien_nom', 'anesthesiste_nom', 'aide_nom')
    list_filter = ('created_at',)


@admin.register(ActeMedical)
class ActeMedicalAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
    )
    search_fields = ('libelle', 'chirurgien_nom', 'anesthesiste_nom')
    list_filter = ('type_acte', 'created_at')


@admin.register(ActeMedicalSimple)
class ActeMedicalSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
        'repartition_detaillee',
    )
    search_fields = ('libelle', 'chirurgien_nom', 'aide_nom')
    list_filter = ('type_acte', 'created_at')


@admin.register(ActeMedicalIntermediaire)
class ActeMedicalIntermediaireAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'aide_nom', 'aide_montant',
        'created_at',
        'repartition_detaillee',
    )
    search_fields = ('libelle', 'chirurgien_nom', 'instrumentiste_nom', 'aide_nom')
    list_filter = ('type_acte', 'created_at')
