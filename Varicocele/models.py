from django.db import models
from decimal import Decimal

class Varicocele(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    chirurgien = models.CharField(max_length=255)
    aide = models.CharField(max_length=255)
    panseur = models.CharField(max_length=255)

    @property
    def maison(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.50'), 2)
        return Decimal('0.00')

    @property
    def montant_acteurs(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.50'), 2)
        return Decimal('0.00')

    @property
    def chirurgien_part(self):
        return round(self.montant_acteurs * Decimal('0.80'), 2)

    @property
    def aide_part(self):
        return round(self.montant_acteurs * Decimal('0.15'), 2)

    @property
    def panseur_part(self):
        return round(self.montant_acteurs * Decimal('0.05'), 2)

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
