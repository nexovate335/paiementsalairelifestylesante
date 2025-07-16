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

ANNEE_CHOICES = [(str(annee), str(annee)) for annee in range(2020, datetime.now().year + 10)]

class FichePrestation(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    poste = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)

    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    consultations = models.IntegerField(blank=True, null=True)
    echographie_prescripteur = models.IntegerField(blank=True, null=True)
    echographie_acteur = models.IntegerField(blank=True, null=True)
    pourcentage_hospitalisation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accouchements = models.IntegerField(blank=True, null=True)
    chirurgie = models.IntegerField(blank=True, null=True)
    aides = models.IntegerField(blank=True, null=True)
    prescription_labo = models.IntegerField(blank=True, null=True)
    bonus_pharmacie = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    anciennete = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def total_avant_retenu(self):
        fields = [
            self.consultations,
            self.echographie_prescripteur,
            self.echographie_acteur,
            self.pourcentage_hospitalisation,
            self.accouchements,
            self.chirurgie,
            self.aides,
            self.prescription_labo,
            self.bonus_pharmacie,
            self.prime_transport,
            self.anciennete,
        ]
        return sum([f or 0 for f in fields])

    def total_apres_retenu(self):
        return self.total_avant_retenu() - (self.avance_salaire or 0)

    def net_a_payer(self):
        return self.total_apres_retenu()

    def __str__(self):
        return f"{self.nom} - {self.mois} {self.annee}"
