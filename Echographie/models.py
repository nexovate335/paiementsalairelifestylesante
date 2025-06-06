from django.db import models
from decimal import Decimal

class PaiementEchographie(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        montant = self.montant_total or 0

        msn_pct = Decimal('0.70')
        acteur_pct = Decimal('0.25')
        aide_pct = Decimal('0.05')

        self.msn_montant = montant * msn_pct
        self.acteur_montant = montant * acteur_pct
        self.aide_montant = montant * aide_pct

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle} - {self.montant_total} FCFA"
