from django.db import models
from decimal import Decimal

# -------------------------------
# HOSPITALISATION & ACTEURS
# -------------------------------

class Hospitalisation(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        self.msn_montant = self.montant_total * Decimal('0.70')
        montant_restant = self.montant_total * Decimal('0.30')

        acteurs = self.acteurs.all()
        nombre_acteurs = acteurs.count()

        if nombre_acteurs > 0:
            part = montant_restant / nombre_acteurs
            for acteur in acteurs:
                acteur.montant = part
                acteur.save()

        self.save()

    def __str__(self):
        return f"Hospitalisation - {self.libelle}"


class ActeurHospitalisation(models.Model):
    hospitalisation = models.ForeignKey(
        Hospitalisation,
        on_delete=models.PROTECT,
        related_name='acteurs'
    )
    nom = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nom} ({self.hospitalisation.libelle})"


# -------------------------------
# IVA / IVL
# -------------------------------

class IVA_IVL(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')
        self.acteur_montant = montant * Decimal('0.25')
        self.aide_montant = montant * Decimal('0.05')

    def __str__(self):
        return f"IVA/IVL - {self.libelle}"

# -------------------------------
# MONITORAGE
# -------------------------------

class Monitorage(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')  # ✅ 70% pour MSN
        self.acteur_montant = montant * Decimal('0.30')  # ✅ 30% pour acteur

    def __str__(self):
        return f"Monitorage - {self.libelle}"

# -------------------------------
# Myomectomie
# -------------------------------

class Myomectomie(models.Model):
    libelle = models.CharField(max_length=255, )
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    anesthesiste_nom = models.CharField(max_length=255)
    anesthesiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.75')

        acteurs_total = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs_total * Decimal('0.45')
        self.anesthesiste_montant = acteurs_total * Decimal('0.28')
        self.aide_montant = acteurs_total * Decimal('0.17')
        self.instrumentiste_montant = acteurs_total * Decimal('0.05')
        self.panseur_montant = acteurs_total * Decimal('0.05')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.anesthesiste_nom}: {self.anesthesiste_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Myomectomie - {self.libelle}"

# -------------------------------
# HernieOmbilicale
# -------------------------------

class HernieOmbilicale(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.60')
        self.aide_montant = acteurs_total * Decimal('0.30')
        self.panseur_montant = acteurs_total * Decimal('0.10')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Hernie Ombilicale - {self.libelle}"


# -------------------------------
# Polype
# -------------------------------

class Polype(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.60')
        self.aide_montant = acteurs_total * Decimal('0.30')
        self.panseur_montant = acteurs_total * Decimal('0.10')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Polype - {self.libelle}"

# -------------------------------
# HVV
# -------------------------------

class HVV(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    anesthesiste_nom = models.CharField(max_length=255)
    anesthesiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.75')

        acteurs_total = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs_total * Decimal('0.40')
        self.anesthesiste_montant = acteurs_total * Decimal('0.25')
        self.aide_montant = acteurs_total * Decimal('0.23')
        self.instrumentiste_montant = acteurs_total * Decimal('0.06')
        self.panseur_montant = acteurs_total * Decimal('0.06')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.anesthesiste_nom}: {self.anesthesiste_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"HVV - {self.libelle}"


# -------------------------------
# HVH
# -------------------------------

class HVH(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    anesthesiste_nom = models.CharField(max_length=255)
    anesthesiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.75')

        acteurs_total = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs_total * Decimal('0.45')
        self.anesthesiste_montant = acteurs_total * Decimal('0.28')
        self.aide_montant = acteurs_total * Decimal('0.17')
        self.instrumentiste_montant = acteurs_total * Decimal('0.05')
        self.panseur_montant = acteurs_total * Decimal('0.05')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.anesthesiste_nom}: {self.anesthesiste_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"HVH - {self.libelle}"


# -------------------------------
# PYRACIDECTOMIE
# -------------------------------

class Pyracidectomie(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.15')
        self.instrumentiste_montant = acteurs_total * Decimal('0.035')
        self.panseur_montant = acteurs_total * Decimal('0.035')
        self.aide_montant = acteurs_total * Decimal('0.08')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Pyracidectomie - {self.libelle}"

# -------------------------------
# NODULECTOMIE SEIN
# -------------------------------

class NodulectomieSein(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.15')
        self.instrumentiste_montant = acteurs_total * Decimal('0.035')
        self.panseur_montant = acteurs_total * Decimal('0.035')
        self.aide_montant = acteurs_total * Decimal('0.08')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Nodulectomie sein - {self.libelle}"

# -------------------------------
# CONISATION
# -------------------------------

class Conisation(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.15')
        self.instrumentiste_montant = acteurs_total * Decimal('0.035')
        self.panseur_montant = acteurs_total * Decimal('0.035')
        self.aide_montant = acteurs_total * Decimal('0.08')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Conisation - {self.libelle}"

# -------------------------------
# MALE ABDOMINALE
# -------------------------------

class MaleAbdominale(models.Model):
    libelle = models.CharField(max_length=255, )
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    anesthesiste_nom = models.CharField(max_length=255)
    anesthesiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    instrumentiste_nom = models.CharField(max_length=255)
    instrumentiste_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.75')

        acteurs_total = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs_total * Decimal('0.45')
        self.anesthesiste_montant = acteurs_total * Decimal('0.28')
        self.aide_montant = acteurs_total * Decimal('0.17')
        self.instrumentiste_montant = acteurs_total * Decimal('0.05')
        self.panseur_montant = acteurs_total * Decimal('0.05')

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.anesthesiste_nom}: {self.anesthesiste_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"

    def __str__(self):
        return f"Myomectomie - {self.libelle}"

# -------------------------------
# ENVENTRIATION
# -------------------------------

class Eventration(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.60')
        self.aide_montant = acteurs_total * Decimal('0.30')
        self.panseur_montant = acteurs_total * Decimal('0.10')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Eventration - {self.libelle}"

# -------------------------------
# CONISATION
# -------------------------------

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
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TPI - {self.libelle}"

# -------------------------------
# MANCHESTER
# -------------------------------
class Manchester(models.Model):
    libelle = models.CharField(max_length=255, default='Manchester')
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

        acteurs = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs * Decimal('0.45')
        self.anesthesiste_montant = acteurs * Decimal('0.28')
        self.aide_montant = acteurs * Decimal('0.17')
        self.instrumentiste_montant = acteurs * Decimal('0.05')
        self.panseur_montant = acteurs * Decimal('0.05')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Manchester - {self.libelle}"

# -------------------------------
# SYNECHIE
# -------------------------------

class Synechie(models.Model):
    libelle = models.CharField(max_length=255, default='Synechie')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255, blank=True, null=True)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255, blank=True, null=True)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs * Decimal('0.60')
        self.aide_montant = acteurs * Decimal('0.30')
        self.panseur_montant = acteurs * Decimal('0.10')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Synechie - {self.libelle}"

# -------------------------------
# CAUTHERISATION
# -------------------------------
class Cautherisation(models.Model):
    libelle = models.CharField(max_length=255, default='Cautherisation')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    chirurgien_nom = models.CharField(max_length=255, blank=True, null=True)
    chirurgien_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    panseur_nom = models.CharField(max_length=255, blank=True, null=True)
    panseur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs_total = montant * Decimal('0.30')
        self.chirurgien_montant = acteurs_total * Decimal('0.60')
        self.aide_montant = acteurs_total * Decimal('0.30')
        self.panseur_montant = acteurs_total * Decimal('0.10')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cautherisation - {self.libelle}"

