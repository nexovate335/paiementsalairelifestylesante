from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Pharmacie(models.Model):
    libelle = models.CharField(max_length=255)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def benefice(self):
        if self.prix_vente:
            # Calcul : Prix de vente - (Prix de vente / 1.5)
            result = self.prix_vente - (self.prix_vente / Decimal('1.5'))
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')

    @property
    def maison(self):
        return (self.benefice * Decimal('0.80')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def controleur(self):
        return (self.benefice * Decimal('0.04')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def vendeur(self):
        return (self.benefice * Decimal('0.10')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def prescripteur(self):
        return (self.benefice * Decimal('0.06')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.libelle} - {self.prix_vente} FCFA"
