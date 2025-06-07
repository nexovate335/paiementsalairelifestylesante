from decimal import Decimal
from django.db import models

class ActeORL(models.Model):
    libelle = models.CharField(max_length=255)
    montant_tt = models.DecimalField(max_digits=10, decimal_places=2)
    montant_msn = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_acteur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.montant_tt:
            self.montant_msn = self.montant_tt * Decimal('0.4')
            self.montant_acteur = self.montant_tt * Decimal('0.6')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle
