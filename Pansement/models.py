from django.db import models
from decimal import Decimal

class Pansement(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def maison(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.75'), 2)
        return Decimal('0.00')

    @property
    def acteur(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.25'), 2)
        return Decimal('0.00')

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
