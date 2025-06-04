from django.db import models
from decimal import Decimal

class Cesarienne(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    chirurgien = models.CharField(max_length=255, null=True, blank=True)
    aide = models.CharField(max_length=255, null=True, blank=True)
    anesthesiste = models.CharField(max_length=255, null=True, blank=True)
    panseur = models.CharField(max_length=255, null=True, blank=True)
    instrumentiste = models.CharField(max_length=255, null=True, blank=True)
    pediatre = models.CharField(max_length=255, null=True, blank=True)
    sf = models.CharField("Sage-Femme", max_length=255, null=True, blank=True)

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
    def part_chirurgien(self):
        return round(self.total_acteurs * Decimal('0.28'), 2)

    @property
    def part_aide(self):
        return round(self.total_acteurs * Decimal('0.15'), 2)

    @property
    def part_anesthesiste(self):
        return round(self.total_acteurs * Decimal('0.21'), 2)

    @property
    def part_panseur(self):
        return round(self.total_acteurs * Decimal('0.10'), 2)

    @property
    def part_instrumentiste(self):
        return round(self.total_acteurs * Decimal('0.10'), 2)

    @property
    def part_pediatre(self):
        return round(self.total_acteurs * Decimal('0.08'), 2)

    @property
    def part_sf(self):
        return round(self.total_acteurs * Decimal('0.08'), 2)

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
