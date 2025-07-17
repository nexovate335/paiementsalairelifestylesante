from decimal import Decimal
from django.db import models

class Pansement(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField("Montant total", max_digits=10, decimal_places=2, null=True, blank=True)

    montant_maison = models.DecimalField("Montant Maison", max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    type_maison = models.CharField(max_length=20, default="maison", editable=False)

    acteur = models.CharField("Acteur", max_length=255, null=True, blank=True)
    montant_acteur = models.DecimalField("Montant Acteur", max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if self.montantTT:
            self.montant_maison = round(self.montantTT * Decimal('0.75'), 2)
            self.montant_acteur = round(self.montantTT * Decimal('0.25'), 2)
        else:
            self.montant_maison = Decimal('0.00')
            self.montant_acteur = Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
