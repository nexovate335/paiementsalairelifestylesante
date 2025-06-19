from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
import calendar

class ChargeObligatoire(models.Model):
    libelle = models.CharField(max_length=255)
    depense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mois = models.DateField(auto_now_add=True)

    def mois_formate(self):
        return self.mois.strftime("%B %Y")

    def __str__(self):
        return f"{self.libelle} - {self.depense} FCFA"

    class Meta:
        verbose_name = "Charge Obligatoire"
        verbose_name_plural = "Charges Obligatoires"


class MontantTotal(models.Model):
    montant = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.montant} FCFA - {self.date}"

    class Meta:
        verbose_name = "Montant Total"
        verbose_name_plural = "Montants Totaux"


# Classe de traitement (calculs)
class TraitementChargeObligatoire:

    @staticmethod
    def depense_totale():
        total = ChargeObligatoire.objects.aggregate(total=Sum('depense'))['total']
        return total or Decimal('0.00')

    @staticmethod
    def total_du_mois(mois, annee):
        total = ChargeObligatoire.objects.filter(
            mois__month=mois,
            mois__year=annee
        ).aggregate(total=Sum('depense'))['total']
        return total or Decimal('0.00')

    @staticmethod
    def total_mois_actuel():
        today = timezone.now()
        return TraitementChargeObligatoire.total_du_mois(today.month, today.year)

    @staticmethod
    def mois_actuel_format():
        today = timezone.now()
        mois_nom = calendar.month_name[today.month].capitalize()
        return f"{mois_nom} {today.year}"

    @staticmethod
    def dernier_montant_total():
        dernier = MontantTotal.objects.order_by('-date').first()
        if dernier:
            return dernier.montant
        return Decimal('0.00')

    @classmethod
    def calculer_reste(cls):
        montant_total = cls.dernier_montant_total()
        depense = cls.depense_totale()
        reste = montant_total - depense
        return reste
