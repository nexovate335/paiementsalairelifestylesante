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

# -----------------------------
# Base Mixin pour la répartition
# -----------------------------
class RepartitionMixin:
    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')

        if getattr(self, 'type', '') == 'orl':
            msn_pct = Decimal('0.60')
            acteur_pct = Decimal('0.40')
            aide_pct = Decimal('0.00')
        else:
            msn_pct = Decimal('0.70')
            acteur_pct = Decimal('0.25')
            aide_pct = Decimal('0.05')

        self.msn_montant = montant * msn_pct
        self.acteur_montant = montant * acteur_pct
        self.aide_montant = montant * aide_pct

# -----------------------------
# Classe Consultation
# -----------------------------
class Consultation(models.Model, RepartitionMixin):
    TYPE_CHOICES = [
        ('generale', 'Consultation Générale'),
        ('prenatale', 'Consultation Prénatale'),
        ('pediatrique', 'Consultation Pédiatrique'),
        ('anesthesique', 'Consultation Anesthésique'),
        ('orl', 'Consultation ORL'),
    ]

    libelle = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.libelle}"


# -----------------------------
# Modèle Certificat Médical
# -----------------------------
class CertificatMedical(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    # Maison de santé
    msn_nom = models.CharField(max_length=255)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Acteur
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')
        self.acteur_montant = montant * Decimal('0.30')
        # self.save() volontairement non appelé ici

    def __str__(self):
        return f"Certificat - {self.libelle}"
