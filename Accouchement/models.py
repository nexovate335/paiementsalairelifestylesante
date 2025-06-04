from django.db import models
from decimal import Decimal

class Accouchement(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    medecin = models.CharField("Médecin", max_length=255, null=True, blank=True)
    sf = models.CharField("Sage-femme", max_length=255, null=True, blank=True)
    aide = models.CharField("Aide", max_length=255, null=True, blank=True)
    pediatre = models.CharField("Pédiatre", max_length=255, null=True, blank=True)

    @property
    def maison(self):
        if self.montantTT:
            return round(self.montantTT * Decimal('0.65'), 2)
        return Decimal('0.00')

    @property
    def total_acteurs(self):
        if self.montantTT:
            return round(self.montantTT * Decimal('0.35'), 2)
        return Decimal('0.00')

    @property
    def part_medecin(self):
        return round(self.total_acteurs * Decimal('0.4286'), 2)  # 15% / 35% ≈ 42.86%

    @property
    def part_sf(self):
        return round(self.total_acteurs * Decimal('0.2857'), 2)  # 10% / 35% ≈ 28.57%

    @property
    def part_aide(self):
        return round(self.total_acteurs * Decimal('0.1429'), 2)  # 5% / 35% ≈ 14.29%

    @property
    def part_pediatre(self):
        return round(self.total_acteurs * Decimal('0.1429'), 2)  # 5% / 35% ≈ 14.29%

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
