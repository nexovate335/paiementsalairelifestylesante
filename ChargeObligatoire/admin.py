from django.contrib import admin, messages
from django.db.models import Sum
from datetime import date

from .models import ChargeObligatoire, MontantTotal, TraitementChargeObligatoire


@admin.register(ChargeObligatoire)
class ChargeObligatoireAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'depense', 'mois_formate')
    list_filter = ('mois', 'libelle')
    search_fields = ('libelle',)
    actions = ['afficher_total_mensuel', 'afficher_total_general']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            total_mensuel = TraitementChargeObligatoire.total_mois_actuel()
            mois_actuel = TraitementChargeObligatoire.mois_actuel_format()
            reste = TraitementChargeObligatoire.calculer_reste()

            response.context_data['total_mensuel'] = total_mensuel
            response.context_data['mois_actuel'] = mois_actuel
            response.context_data['reste'] = reste

        except (AttributeError, KeyError):
            pass

        return response

    def afficher_total_mensuel(self, request, queryset):
        total = TraitementChargeObligatoire.total_mois_actuel()
        messages.info(
            request,
            f"Total des dépenses pour {TraitementChargeObligatoire.mois_actuel_format()} : {total} FCFA"
        )

    afficher_total_mensuel.short_description = "Afficher total du mois actuel"

    def afficher_total_general(self, request, queryset):
        total = TraitementChargeObligatoire.depense_totale()
        messages.success(request, f"Total général des dépenses : {total} FCFA")

    afficher_total_general.short_description = "Afficher total général"


@admin.register(MontantTotal)
class MontantTotalAdmin(admin.ModelAdmin):
    list_display = ('montant', 'date')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            total_mensuel = TraitementChargeObligatoire.total_mois_actuel()
            mois_actuel = TraitementChargeObligatoire.mois_actuel_format()

            response.context_data['total_mensuel'] = total_mensuel
            response.context_data['mois_actuel'] = mois_actuel

        except (AttributeError, KeyError):
            pass

        return response
