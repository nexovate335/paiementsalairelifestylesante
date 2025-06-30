from django.contrib import admin
from django.db.models import Sum
from decimal import Decimal
from .models import (
    DocteurSalaire,
    ParaMedicoSalaire,
    PreleveurSalaire,
    PratiqueurSalaire,
    PrimeTransport,
)

class SalaireBaseAdmin(admin.ModelAdmin):
    list_display = ('nom_personne', 'fonction', 'designation', 'nombre', 'montant_total', 'pourcentage', 'gain', 'mois', 'annee')
    list_filter = ('mois', 'annee', 'fonction')
    search_fields = ('nom_personne', 'designation', 'fonction')
    ordering = ['-annee', '-mois']

    # Action personnalisée pour totaliser les gains d'un employé sur une période
    actions = ['totaliser_gains']

    def totaliser_gains(self, request, queryset):
        # Récupérer nom_personne, mois, annee depuis la sélection
        # Pour simplifier, on totalise par personne, mois, année des objets sélectionnés

        from django.http import HttpResponse
        from collections import defaultdict

        resultats = defaultdict(lambda: Decimal('0.00'))

        for obj in queryset:
            cle = (obj.nom_personne, obj.mois, obj.annee)
            resultats[cle] += obj.gain

        lignes = ["Nom Personne | Mois | Année | Total Gains (sans prime transport)"]
        for (nom, mois, annee), total in resultats.items():
            lignes.append(f"{nom} | {mois} | {annee} | {total:.2f}")

        response_text = "\n".join(lignes)
        return HttpResponse(response_text, content_type="text/plain")

    totaliser_gains.short_description = "Afficher total des gains sélectionnés (hors prime transport)"


@admin.register(DocteurSalaire)
class DocteurSalaireAdmin(SalaireBaseAdmin):
    pass


@admin.register(ParaMedicoSalaire)
class ParaMedicoSalaireAdmin(SalaireBaseAdmin):
    pass


@admin.register(PreleveurSalaire)
class PreleveurSalaireAdmin(SalaireBaseAdmin):
    pass


@admin.register(PratiqueurSalaire)
class PratiqueurSalaireAdmin(SalaireBaseAdmin):
    pass


@admin.register(PrimeTransport)
class PrimeTransportAdmin(admin.ModelAdmin):
    list_display = ('nom_personne', 'fonction', 'nombre_total', 'arrivee_true', 'arrivee_false', 'montant', 'prime_totale', 'mois', 'annee')
    list_filter = ('mois', 'annee', 'fonction')
    search_fields = ('nom_personne', 'fonction')
    ordering = ['-annee', '-mois']

    def prime_totale(self, obj):
        return obj.prime_totale()
    prime_totale.short_description = 'Prime Totale'
