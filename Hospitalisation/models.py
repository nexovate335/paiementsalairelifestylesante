from django.db import models
from decimal import Decimal

# === Paiements simples ===
from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class PaiementHospitalisation(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_nom = models.CharField(max_length=255)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')

        acteurs = self.acteurhospitalisation_set.all()
        nb_acteurs = acteurs.count()

        if nb_acteurs > 0:
            part_individuelle = (montant * Decimal('0.30')) / nb_acteurs
            part_individuelle = part_individuelle.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            for acteur in acteurs:
                acteur.montant_recu = part_individuelle
                acteur.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calcul_repartition()

    def __str__(self):
        return f"Hospitalisation - {self.libelle}"

    def repartition_detaillee(self):
        return ", ".join([f"{a.nom}: {a.montant_recu} FCFA" for a in self.acteurhospitalisation_set.all()])
    repartition_detaillee.short_description = "Répartition Acteurs"


class ActeurHospitalisation(models.Model):
    paiement = models.ForeignKey(PaiementHospitalisation, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    montant_recu = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nom} ({self.montant_recu} FCFA)"


class PaiementIVA_IVL(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.70')
        self.acteur_montant = montant * Decimal('0.25')
        self.aide_montant = montant * Decimal('0.05')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"IVA/IVL - {self.libelle}"
    


class PaiementMonitorage(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

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


# === Actes chirurgicaux complexes ===

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

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"HVV - {self.libelle}"

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.anesthesiste_nom}: {self.anesthesiste_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"


# === Actes génériques (groupés par complexité) ===

class ActeMedical(models.Model):
    TYPE_ACTES = [
        ("Myomectomie", "Myomectomie"),
        ("HVH", "HVH"),
        ("Male abdominale", "Male abdominale"),
        ("TPI", "TPI"),
        ("Manchester", "Manchester"),
    ]

    type_acte = models.CharField(max_length=100, choices=TYPE_ACTES)
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
        acteurs_total = montant * Decimal('0.25')
        self.chirurgien_montant = acteurs_total * Decimal('0.45')
        self.anesthesiste_montant = acteurs_total * Decimal('0.28')
        self.aide_montant = acteurs_total * Decimal('0.17')
        self.instrumentiste_montant = acteurs_total * Decimal('0.05')
        self.panseur_montant = acteurs_total * Decimal('0.05')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_acte} - {self.libelle}"


class ActeMedicalSimple(models.Model):
    TYPE_ACTES = [
        ("Hernie Ombilicale", "Hernie Ombilicale"),
        ("Polype", "Polype"),
        ("Eventration", "Eventration"),
        ("Synechie", "Synechie"),
        ("Cauthérisation", "Cauthérisation"),
    ]

    type_acte = models.CharField(max_length=100, choices=TYPE_ACTES)
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
        return f"{self.type_acte} - {self.libelle}"

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA"
        )


class ActeMedicalIntermediaire(models.Model):
    TYPE_ACTES = [
        ("Pyracidectomie", "Pyracidectomie"),
        ("Nodulectomie du Sein", "Nodulectomie du Sein"),
        ("Conisation", "Conisation"),
    ]

    type_acte = models.CharField(max_length=100, choices=TYPE_ACTES)
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

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_acte} - {self.libelle}"

    def repartition_detaillee(self):
        return (
            f"{self.chirurgien_nom}: {self.chirurgien_montant} FCFA, "
            f"{self.instrumentiste_nom}: {self.instrumentiste_montant} FCFA, "
            f"{self.panseur_nom}: {self.panseur_montant} FCFA, "
            f"{self.aide_nom}: {self.aide_montant} FCFA"
        )
    repartition_detaillee.short_description = "Répartition détaillée"
