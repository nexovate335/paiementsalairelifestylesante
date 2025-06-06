from django.contrib import admin
from .models import (
    Hospitalisation, ActeurHospitalisation, Polype, HVV, Pyracidectomie, Conisation, Eventration,
    IVA_IVL, Monitorage, Myomectomie, HernieOmbilicale, HVH, NodulectomieSein, MaleAbdominale, TPI,
    Manchester, Synechie, Cautherisation
)

# -----------------------------
# ADMIN HOSPITALISATION
# -----------------------------

class ActeurHospitalisationInline(admin.TabularInline):
    model = ActeurHospitalisation
    extra = 0
    readonly_fields = ('montant',)
    verbose_name = "Acteur"
    verbose_name_plural = "Acteurs (répartition des 30%)"

@admin.register(Hospitalisation)
class HospitalisationAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_montant', 'afficher_acteurs', 'created_at')
    inlines = [ActeurHospitalisationInline]
    readonly_fields = ('msn_montant', 'created_at')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Répartition après enregistrement complet (acteurs inclus)
        form.instance.calcul_repartition()

    def afficher_acteurs(self, obj):
        return ", ".join([f"{a.nom}: {a.montant} FCFA" for a in obj.acteurs.all()]) or "Aucun acteur"

    afficher_acteurs.short_description = "Répartition des 30% entre acteurs"


# -----------------------------
# ADMIN IVA / IVL
# -----------------------------

@admin.register(IVA_IVL)
class IVAIVLAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total',
        'msn_montant',
        'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant',
        'created_at'
    )
    readonly_fields = ('msn_montant', 'acteur_montant', 'aide_montant', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


# -----------------------------
# ADMIN MONITORAGE
# -----------------------------

@admin.register(Monitorage)
class MonitorageAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total',
        'msn_montant',
        'acteur_nom', 'acteur_montant',
        'created_at'
    )
    readonly_fields = ('msn_montant', 'acteur_montant', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN Myomectomie
# -----------------------------

@admin.register(Myomectomie)
class MyomectomieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant', 'chirurgien_montant', 'anesthesiste_montant',
        'aide_montant', 'instrumentiste_montant', 'panseur_montant', 'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN HernieOmbilicale
# -----------------------------

@admin.register(HernieOmbilicale)
class HernieOmbilicaleAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant', 'chirurgien_montant', 'aide_montant', 'panseur_montant', 'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN POLYPE
# -----------------------------

@admin.register(Polype)
class PolypeAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant', 'chirurgien_montant', 'aide_montant', 'panseur_montant', 'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN HVV
# -----------------------------

@admin.register(HVV)
class HVVAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant', 'anesthesiste_montant', 'aide_montant', 'instrumentiste_montant', 'panseur_montant',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


# -----------------------------
# ADMIN HVH
# -----------------------------

@admin.register(HVH)
class HVHAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant', 'anesthesiste_montant', 'aide_montant', 'instrumentiste_montant', 'panseur_montant',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


# -----------------------------
# ADMIN PYRACIDECTOMIE
# -----------------------------

@admin.register(Pyracidectomie)
class PyracidectomieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant', 'instrumentiste_montant', 'panseur_montant', 'aide_montant',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)


# -----------------------------
# ADMIN MODULECTOMIE SEIN
# -----------------------------

@admin.register(NodulectomieSein)
class NodulectomieSeinAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant', 'instrumentiste_montant', 'panseur_montant', 'aide_montant',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN CONISATION
# -----------------------------

@admin.register(Conisation)
class ConisationAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant', 'instrumentiste_montant', 'panseur_montant', 'aide_montant',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN MAL ABDOMINALE
# -----------------------------

@admin.register(MaleAbdominale)
class MaleAbdominaleAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at'
    )
    readonly_fields = (
        'msn_montant', 'chirurgien_montant', 'anesthesiste_montant',
        'aide_montant', 'instrumentiste_montant', 'panseur_montant', 'created_at',
    )

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

# -----------------------------
# ADMIN MONITORAGE
# -----------------------------

@admin.register(Eventration)
class EventrationAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant',
        'aide_montant',
        'panseur_montant'
    )

# -----------------------------
# ADMIN TPI
# -----------------------------

@admin.register(TPI)
class TPIAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant'
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant',
        'anesthesiste_montant',
        'aide_montant',
        'instrumentiste_montant',
        'panseur_montant'
    )

# -----------------------------
# ADMIN MANCHESTER
# -----------------------------

@admin.register(Manchester)
class ManchesterAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant',
        'anesthesiste_montant',
        'aide_montant',
        'instrumentiste_montant',
        'panseur_montant',
    )

# -----------------------------
# ADMIN SYNECHIE
# -----------------------------

@admin.register(Synechie)
class SynechieAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant',
        'aide_montant',
        'panseur_montant',
    )

# -----------------------------
# ADMIN CAUTHERISATION
# -----------------------------

@admin.register(Cautherisation)
class CautherisationAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
    )
    readonly_fields = (
        'msn_montant',
        'chirurgien_montant',
        'aide_montant',
        'panseur_montant',
    )

