from django.db import models
from decimal import Decimal


# -----------------------------
# Modèle Consultation
# -----------------------------
class Consultation(models.Model):
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

    # Maison de santé
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Acteur principal
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Aide facultative
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')

        # Répartition spécifique si ORL
        if self.type == 'orl':
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

    def __str__(self):
        return f"{self.get_type_display()} - {self.libelle}"


# -----------------------------
# Modèle Certificat Médical
# -----------------------------
class CertificatMedical(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

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
