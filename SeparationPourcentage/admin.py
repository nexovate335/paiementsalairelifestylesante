from django.contrib import admin
from decimal import Decimal  # ← Importer Decimal pour remplacer les float
from .models import SeparationPourcentage
from .forms import SeparationPourcentageForm
from ChargeObligatoire.models import TraitementChargeObligatoire


@admin.register(SeparationPourcentage)
class SeparationPourcentageAdmin(admin.ModelAdmin):
    form = SeparationPourcentageForm
    list_display = ('date_calcul', 'reste_a_payer', 'tresor_gu', 'salaire_dg')
    readonly_fields = [field.name for field in SeparationPourcentage._meta.fields]

    def has_add_permission(self, request):
        return True

    def save_model(self, request, obj, form, change):
        # Récupération du reste à payer (en Decimal)
        reste = TraitementChargeObligatoire.calculer_reste()
        obj.reste_a_payer = reste

        # Principaux
        obj.tresor_gu = reste * Decimal('0.25')
        obj.salaire_dg = reste * Decimal('0.10')

        # Investissement
        investissement = reste * Decimal('0.50') / 4
        obj.travaux = investissement
        obj.pharmacie = investissement
        obj.reparation = investissement
        obj.labo = investissement

        # Administration (15% > 40%)
        admin_total = reste * Decimal('0.15') * Decimal('0.40')
        obj.comptable = admin_total * Decimal('0.30')
        obj.chef_personnel = admin_total * Decimal('0.16')
        obj.ag = admin_total * Decimal('0.20')
        obj.surveillant = admin_total * Decimal('0.20')
        obj.informatique = admin_total * Decimal('0.12')

        # Autres services (15% > 60%)
        autre_total = reste * Decimal('0.15') * Decimal('0.60')
        obj.reception_1 = autre_total * Decimal('0.25') / 2
        obj.reception_2 = autre_total * Decimal('0.25') / 2
        obj.caisse_1 = autre_total * Decimal('0.25') / 2
        obj.caisse_2 = autre_total * Decimal('0.25') / 2
        obj.cyril = autre_total * Decimal('0.25') * Decimal('0.16')
        obj.rosine = autre_total * Decimal('0.25') * Decimal('0.09')
        obj.securite_1 = autre_total * Decimal('0.25') / 3
        obj.securite_2 = autre_total * Decimal('0.25') / 3
        obj.securite_3 = autre_total * Decimal('0.25') / 3

        super().save_model(request, obj, form, change)
