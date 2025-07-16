from django.contrib import admin
from .models import ( 
        Accouchement, Cesarienne, CureHernie, HVV,ActeMedical,
        ActeMedicalSimple,ActeMedicalIntermediaire,PaiementIVA_IVL,
        ActeTechnique, Varicocele
    )


class AccouchementAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'medecin', 'part_medecin',
        'sage_femme', 'part_sage_femme',
        'aide', 'part_aide',
        'pediatre', 'part_pediatre',
    )
    readonly_fields = (
        'maison',
        'part_medecin',
        'part_sage_femme',
        'part_aide',
        'part_pediatre',
    )

class CesarienneAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'chirurgien', 'part_chirurgien',
        'anesthesiste', 'part_anesthesiste',
        'aide', 'part_aide',
        'panseur', 'part_panseur',
        'instrumentiste', 'part_instrumentiste',
        'pediatre', 'part_pediatre',
        'sage_femme', 'part_sage_femme',
    )
    readonly_fields = (
        'maison',
        'part_chirurgien',
        'part_anesthesiste',
        'part_aide',
        'part_panseur',
        'part_instrumentiste',
        'part_pediatre',
        'part_sage_femme',
    )


class CureHernieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'chirurgien', 'part_chirurgien',
        'aide', 'part_aide',
        'panseur', 'part_panseur',
    )
    readonly_fields = (
        'maison',
        'part_chirurgien',
        'part_aide',
        'part_panseur',
    )


class HVVAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
    )
    list_filter = ('created_at',)



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
    list_filter = ('type_acte', 'created_at')



class ActeMedicalSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'type_acte', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
        'repartition_detaillee',
    )
    list_filter = ('type_acte', 'created_at')



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
    list_filter = ('type_acte', 'created_at')


class PaiementIVA_IVLAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_montant', 'acteur_nom', 'acteur_montant', 'aide_nom', 'aide_montant', 'created_at')
    list_filter = ('created_at',)


class ActeTechniqueAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'type', 'montant_total',
        'msn_montant', 'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant', 'created_at',
    )
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


@admin.register(Varicocele)
class VaricoceleAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'chirurgien', 'chirurgien_part',
        'aide', 'aide_part',
        'panseur', 'panseur_part',
    )
    readonly_fields = ('maison', 'chirurgien_part', 'aide_part', 'panseur_part')
