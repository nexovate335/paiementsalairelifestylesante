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


class ActeORL(models.Model):
    libelle = models.CharField(max_length=255)
    montant_tt = models.DecimalField(max_digits=10, decimal_places=2)
    montant_msn = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_acteur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.montant_tt:
            self.montant_msn = self.montant_tt * Decimal('0.4')
            self.montant_acteur = self.montant_tt * Decimal('0.6')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle
