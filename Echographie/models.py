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


class ActeMedical(models.Model):
    TYPE_CHOICES = [
        ('echographie', 'Échographie'),  
        # Tu peux en ajouter d'autres ici si besoin
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')

        # Répartition standard
        msn_pct = Decimal('0.70')
        acteur_pct = Decimal('0.25')
        aide_pct = Decimal('0.05')

        self.msn_montant = montant * msn_pct
        self.acteur_montant = montant * acteur_pct
        self.aide_montant = montant * aide_pct

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()} - {self.libelle}"
    

class PaiementMonitorage(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    msn_nom = models.CharField(max_length=255)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')
        self.acteur_montant = montant * Decimal('0.30')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Monitorage - {self.libelle}"