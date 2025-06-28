from django.db import models
from datetime import datetime

# Choix des mois
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

# Choix dynamiques des années (2020 jusqu'à +10 ans après aujourd'hui)
ANNEE_CHOICES = [(str(annee), str(annee)) for annee in range(2020, datetime.now().year + 10)]


class FicheDePaie(models.Model):
    # Informations de l'employé
    nom = models.CharField(max_length=100, null=True, blank=True)
    poste = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)

    # Mois et année de la paie
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    # Prestations
    chirurgie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aide = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    consultations = models.IntegerField(null=True, blank=True)
    prime_laboratoire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonus_prescription_pharmacie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Retenue
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Méthodes de calcul
    def total_avant_retenu(self):
        champs = [
            self.chirurgie,
            self.aide,
            self.prime_laboratoire,
            self.bonus_prescription_pharmacie,
        ]
        return sum([c or 0 for c in champs])

    def total_apres_retenu(self):
        return self.total_avant_retenu() - (self.avance_salaire or 0)

    def net_a_payer(self):
        return self.total_apres_retenu()

    def __str__(self):
        return f"{self.nom} - {self.mois} {self.annee}"
