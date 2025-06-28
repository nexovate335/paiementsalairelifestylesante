from django.contrib import admin, messages
from django.db.models import Sum
from datetime import date
from django.utils import formats
from datetime import datetime

from .models import ChargeObligatoire, MontantTotal, TraitementChargeObligatoire


def format_mois_annee(mois, annee):
    dt = datetime(year=annee, month=mois, day=1)
    return formats.date_format(dt, "F Y")


@admin.register(ChargeObligatoire)
class ChargeObligatoireAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'depense', 'mois_formate')
    list_filter = ('mois', 'annee', 'libelle')
    search_fields = ('libelle',)
    actions = ['afficher_total_mensuel', 'afficher_total_general']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            total_mensuel = TraitementChargeObligatoire.total_mois_actuel()
            today = date.today()
            mois_actuel = format_mois_annee(today.month, today.year)
            reste = TraitementChargeObligatoire.calculer_reste()

            response.context_data['total_mensuel'] = total_mensuel
            response.context_data['mois_actuel'] = mois_actuel
            response.context_data['reste'] = reste

        except (AttributeError, KeyError):
            pass

        return response

    def afficher_total_mensuel(self, request, queryset):
        total = TraitementChargeObligatoire.total_mois_actuel()
        today = date.today()
        mois_actuel = format_mois_annee(today.month, today.year)
        messages.info(
            request,
            f"Total des dépenses pour {mois_actuel} : {total} FCFA"
        )

    afficher_total_mensuel.short_description = "Afficher total du mois actuel"

    def afficher_total_general(self, request, queryset):
        total = TraitementChargeObligatoire.depense_totale()
        messages.success(request, f"Total général des dépenses : {total} FCFA")

    afficher_total_general.short_description = "Afficher total général"


@admin.register(MontantTotal)
class MontantTotalAdmin(admin.ModelAdmin):
    list_display = ('montant', 'mois_formate')
    list_filter = ('mois', 'annee')

    def mois_formate(self, obj):
        return format_mois_annee(obj.mois, obj.annee)

    mois_formate.short_description = "Période"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            total_mensuel = TraitementChargeObligatoire.total_mois_actuel()
            today = date.today()
            mois_actuel = format_mois_annee(today.month, today.year)

            response.context_data['total_mensuel'] = total_mensuel
            response.context_data['mois_actuel'] = mois_actuel

        except (AttributeError, KeyError):
            pass

        return response
