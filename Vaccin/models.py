from django.db import models
from decimal import Decimal
from datetime import datetime

MOIS_CHOICES = [
    ('janvier', 'Janvier'),
    ('fevrier', 'Février'),
    ('mars', 'Mars'),
    ('avril', 'Avril'),
    ('mai', 'Mai'),
    ('juin', 'Juin'),
    ('juillet', 'Juillet'),
    ('aout', 'Août'),
    ('septembre', 'Septembre'),
    ('octobre', 'Octobre'),
    ('novembre', 'Novembre'),
    ('decembre', 'Décembre'),
]

ANNEE_CHOICES = [(str(annee), str(annee)) for annee in range(2020, datetime.now().year + 20)]


class Vaccin(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    nom_acteur1 = models.CharField(max_length=255, null=True, blank=True)
    nom_acteur2 = models.CharField(max_length=255, null=True, blank=True)
    nom_acteur3 = models.CharField(max_length=255, null=True, blank=True)

    @property
    def maison(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.70'), 2)
        return Decimal('0.00')

    @property
    def acteurs_total(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.30'), 2)
        return Decimal('0.00')

    @property
    def acteur1_part(self):
        return round(self.acteurs_total * Decimal('0.40'), 2)

    @property
    def acteur2_part(self):
        return round(self.acteurs_total * Decimal('0.40'), 2)

    @property
    def acteur3_part(self):
        return round(self.acteurs_total * Decimal('0.20'), 2)

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
