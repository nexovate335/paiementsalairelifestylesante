from decimal import Decimal
from django.db import models
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


class Pansement(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField("Montant total", max_digits=10, decimal_places=2, null=True, blank=True)

    montant_maison = models.DecimalField("Montant Maison", max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    type_maison = models.CharField(max_length=20, default="maison", editable=False)

    acteur = models.CharField("Acteur", max_length=255, null=True, blank=True)
    montant_acteur = models.DecimalField("Montant Acteur", max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

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
