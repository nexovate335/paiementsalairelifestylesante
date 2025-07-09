from django.contrib import admin
from decimal import Decimal
from .models import SeparationPourcentage
from .forms import SeparationPourcentageForm
from ChargeObligatoire.models import TraitementChargeObligatoire, MontantTotal, ChargeObligatoire


@admin.register(SeparationPourcentage)
class SeparationPourcentageAdmin(admin.ModelAdmin):
    form = SeparationPourcentageForm
    list_display = ('date_calcul', 'mois', 'annee', 'reste_a_payer', 'tresor_gu', 'salaire_dg')

    # Rendre tous les champs readonly sauf `mois` et `annee`
    def get_readonly_fields(self, request, obj=None):
        editable = ['mois', 'annee']
        return [field.name for field in SeparationPourcentage._meta.fields if field.name not in editable]

    def save_model(self, request, obj, form, change):
        # Étape 1 : sauvegarde de base
        super().save_model(request, obj, form, change)

        if not obj.mois or not obj.annee:
            return

        montant = MontantTotal.objects.filter(mois=obj.mois, annee=obj.annee).first()
        montant_total = montant.montant if montant else Decimal('0.00')

        depenses = ChargeObligatoire.objects.filter(mois=obj.mois, annee=obj.annee)
        total_depense = sum((d.depense for d in depenses), Decimal('0.00'))

        reste = montant_total - total_depense
        obj.reste_a_payer = reste

        obj.tresor_gu = reste * Decimal('0.25')
        obj.salaire_dg = reste * Decimal('0.10')

        investissement = reste * Decimal('0.50') / 4
        obj.travaux = investissement
        obj.pharmacie = investissement
        obj.reparation = investissement
        obj.labo = investissement

        admin_total = reste * Decimal('0.15') * Decimal('0.40')
        obj.comptable = admin_total * Decimal('0.30')
        obj.chef_personnel = admin_total * Decimal('0.16')
        obj.ag = admin_total * Decimal('0.20')
        obj.surveillant = admin_total * Decimal('0.20')
        obj.informatique = admin_total * Decimal('0.12')

        autre_total = reste * Decimal('0.15') * Decimal('0.60')
        obj.reception_1 = autre_total * Decimal('0.25') / 2
        obj.reception_2 = autre_total * Decimal('0.25') / 2
        obj.caisse_1 = autre_total * Decimal('0.25') / 2
        obj.caisse_2 = autre_total * Decimal('0.25') / 2
        obj.Menage_1 = autre_total * Decimal('0.12') / 3
        obj.Menage_2 = autre_total * Decimal('0.08') / 3
        obj.Menage_3 = autre_total * Decimal('0.06') / 3
        obj.securite_1 = autre_total * Decimal('0.25') / 3
        obj.securite_2 = autre_total * Decimal('0.25') / 3
        obj.securite_3 = autre_total * Decimal('0.25') / 3

        obj.save()
