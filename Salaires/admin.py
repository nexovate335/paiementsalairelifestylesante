from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from .models import (
    DocteurSalaire,
    PreleveurSalaire,
    PratiqueurSalaire,
    ParaMedicoSalaire,
    PrimeTransport
)

# ✅ Action qui calcule le total des gains regroupé par personne
def calculer_total_gain_par_personne_action(modeladmin, request, queryset):
    resultats = (
        queryset
        .values('nom_personne')
        .annotate(total_gain=Sum('gain'))
    )

    output = "=== Total des gains par personne (pour la sélection) ===\n\n"
    total_general = 0

    for item in resultats:
        nom = item['nom_personne']
        total_gain = item['total_gain'] or 0
        total_general += total_gain
        output += f"👤 {nom} : {total_gain:,} FCFA\n"

    output += f"\n=== Total Général : {total_general:,} FCFA ==="

    return HttpResponse(f"<pre>{output}</pre>")

calculer_total_gain_par_personne_action.short_description = "✅ Calculer TOTAL des gains par personne (regroupé)"

# ✅ Ajout sur tous les ModelAdmins
for ModelAdmin in [DocteurSalaire, PreleveurSalaire, PratiqueurSalaire, ParaMedicoSalaire]:
    admin.site.add_action(calculer_total_gain_par_personne_action)

# ✅ Admin DocteurSalaire
@admin.register(DocteurSalaire)
class DocteurSalaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom_personne', 'fonction', 'designation', 'mois', 'annee',
        'montant', 'nombre', 'montant_total', 'pourcentage', 'gain',
    )
    readonly_fields = ('montant_total', 'pourcentage', 'gain')
    list_filter = ('mois', 'annee', 'nom_personne', 'fonction', 'designation')
    actions = [calculer_total_gain_par_personne_action]

# ✅ Admin PreleveurSalaire
@admin.register(PreleveurSalaire)
class PreleveurSalaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom_personne', 'fonction', 'designation', 'mois', 'annee',
        'montant', 'nombre', 'montant_total', 'pourcentage', 'gain',
    )
    readonly_fields = ('montant_total', 'pourcentage', 'gain')
    list_filter = ('mois', 'annee', 'nom_personne', 'fonction', 'designation')
    actions = [calculer_total_gain_par_personne_action]

# ✅ Admin PratiqueurSalaire
@admin.register(PratiqueurSalaire)
class PratiqueurSalaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom_personne', 'fonction', 'designation', 'mois', 'annee',
        'montant', 'nombre', 'montant_total', 'pourcentage', 'gain',
    )
    readonly_fields = ('montant_total', 'pourcentage', 'gain')
    list_filter = ('mois', 'annee', 'nom_personne', 'fonction', 'designation')
    actions = [calculer_total_gain_par_personne_action]

# ✅ Admin ParaMedicoSalaire
@admin.register(ParaMedicoSalaire)
class ParaMedicoSalaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom_personne', 'fonction', 'designation', 'mois', 'annee',
        'montant', 'nombre', 'montant_total', 'pourcentage', 'gain',
    )
    readonly_fields = ('montant_total', 'pourcentage', 'gain')
    list_filter = ('mois', 'annee', 'nom_personne', 'fonction', 'designation')
    actions = [calculer_total_gain_par_personne_action]

# ✅ Admin PrimeTransport
@admin.register(PrimeTransport)
class PrimeTransportAdmin(admin.ModelAdmin):
    list_display = (
        'nom_personne', 'fonction', 'mois', 'annee',
        'nombre_total', 'arrivee_true', 'arrivee_false', 'montant', 'prime_totale',
    )
    readonly_fields = ('prime_totale',)
    list_filter = ('mois', 'annee', 'nom_personne', 'fonction')

    def prime_totale(self, obj):
        return obj.prime_totale()
