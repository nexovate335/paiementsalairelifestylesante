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

ANNEE_CHOICES = [(str(y), str(y)) for y in range(2020, datetime.now().year + 10)]

class PrestationMensuelle(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    poste = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)

    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    Accouchement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prescriptions_laboratoire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prime_hospitalisation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    anciennete = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    observation = models.TextField(blank=True, null=True)

    def total_avant_retenu(self):
        prestations = [
            self.Accouchement,
            self.actes,
            self.prescriptions_laboratoire,
            self.prime_hospitalisation,
            self.prime_transport,
            self.anciennete,
        ]
        return sum([p or 0 for p in prestations])

    def total_apres_retenu(self):
        return self.total_avant_retenu() - (self.avance_salaire or 0)

    def net_a_payer(self):
        return self.total_apres_retenu()

    def __str__(self):
        return f"{self.nom} - {self.mois} {self.annee}"
