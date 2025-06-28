from django.db import models
from django.utils import timezone, formats
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime

# ✅ Liste des mois en français pour les choix
MOIS_CHOICES = [
    (1, "janvier"), (2, "février"), (3, "mars"), (4, "avril"),
    (5, "mai"), (6, "juin"), (7, "juillet"), (8, "août"),
    (9, "septembre"), (10, "octobre"), (11, "novembre"), (12, "décembre")
]

# ✅ Liste des années (modifiable si besoin)
ANNEE_CHOICES = [(annee, str(annee)) for annee in range(2020, 2036)]

# -------------------------------
# 📌 Modèle des charges obligatoires
# -------------------------------
class ChargeObligatoire(models.Model):
    libelle = models.CharField(max_length=255)
    depense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mois = models.IntegerField(choices=MOIS_CHOICES)
    annee = models.IntegerField(choices=ANNEE_CHOICES, default=2025)

    def mois_formate(self):
        dt = datetime(year=self.annee, month=self.mois, day=1)
        return formats.date_format(dt, "F Y")  # Exemple : juin 2025

    def __str__(self):
        return f"{self.libelle} - {self.depense} FCFA"

    class Meta:
        verbose_name = "Charge Obligatoire"
        verbose_name_plural = "Charges Obligatoires"

# -------------------------------
# 📌 Modèle des montants disponibles
# -------------------------------
class MontantTotal(models.Model):
    montant = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mois = models.IntegerField(choices=MOIS_CHOICES)
    annee = models.IntegerField(choices=ANNEE_CHOICES, default=2025)

    def mois_formate(self):
        dt = datetime(year=self.annee, month=self.mois, day=1)
        return formats.date_format(dt, "F Y")

    def __str__(self):
        return f"{self.montant} FCFA - {self.mois_formate()}"

    class Meta:
        verbose_name = "Montant Total"
        verbose_name_plural = "Montants Totaux"

# -------------------------------
# 📌 Classe de traitement
# -------------------------------
class TraitementChargeObligatoire:

    @staticmethod
    def depense_totale():
        total = ChargeObligatoire.objects.aggregate(total=Sum('depense'))['total']
        return total or Decimal('0.00')

    @staticmethod
    def total_du_mois(mois, annee):
        total = ChargeObligatoire.objects.filter(
            mois=mois,
            annee=annee
        ).aggregate(total=Sum('depense'))['total']
        return total or Decimal('0.00')

    @staticmethod
    def total_mois_actuel():
        today = timezone.now()
        return TraitementChargeObligatoire.total_du_mois(today.month, today.year)

    @staticmethod
    def mois_actuel_format():
        today = timezone.now()
        dt = datetime(year=today.year, month=today.month, day=1)
        return formats.date_format(dt, "F Y")

    @staticmethod
    def dernier_montant_total():
        dernier = MontantTotal.objects.order_by('-annee', '-mois').first()
        return dernier.montant if dernier else Decimal('0.00')

    @classmethod
    def calculer_reste(cls):
        montant_total = cls.dernier_montant_total()
        depense = cls.depense_totale()
        return montant_total - depense
