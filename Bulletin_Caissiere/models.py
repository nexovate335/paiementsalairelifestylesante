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

class FicheDePaie(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    poste = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)

    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    # Prestations
    pourcentage_prestations = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    prime_panier = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    anciennete = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    # Retenues
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def total_avant_retenues(self):
        champs = [
            self.pourcentage_prestations,
            self.prime_panier,
            self.prime_transport,
            self.anciennete
        ]
        return sum([c or 0 for c in champs])  # si champ est None, il prend 0

    def total_retenues(self):
        return self.avance_salaire or 0

    def net_a_payer(self):
        return self.total_avant_retenues() - self.total_retenues()

    def __str__(self):
        return f"{self.nom or 'Fiche'} - {self.mois or ''} {self.annee or ''}"
