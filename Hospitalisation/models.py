from django.db import models
from decimal import Decimal

class PaiementHospitalisation(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')  # Sécurité
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.60')
        self.aide_montant = acteurs_total * Decimal('0.30')
        self.panseur_montant = acteurs_total * Decimal('0.10')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificat - {self.libelle}"
    

class TPI(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255, blank=True, null=True)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    anesthesiste_nom = models.CharField(max_length=255, blank=True, null=True)
    anesthesiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255, blank=True, null=True)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255, blank=True, null=True)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.75')

        part_acteurs = montant * Decimal('0.25')
        self.chirurgien_montant = part_acteurs * Decimal('0.45')
        self.anesthesiste_montant = part_acteurs * Decimal('0.28')
        self.aide_montant = part_acteurs * Decimal('0.17')
        self.instrumentiste_montant = part_acteurs * Decimal('0.05')
        self.panseur_montant = part_acteurs * Decimal('0.05')

    def save(self, *args, **kwargs):
        montant = self.montant_total or 0

        msn_pct = Decimal('0.70')
        acteur_pct = Decimal('0.25')
        aide_pct = Decimal('0.05')

        self.msn_montant = montant * msn_pct
        self.acteur_montant = montant * acteur_pct
        self.aide_montant = montant * aide_pct

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle} - {self.montant_total} FCFA"



class PaiementMonitorage(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

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
        return f"Certificat - {self.libelle}"
