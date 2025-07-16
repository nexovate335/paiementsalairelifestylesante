from django.db import models
from decimal import Decimal

class BlocOperatoire(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        abstract = True  # Classe de base abstraite, pas de table DB ici

    @property
    def maison(self):
        if not self.montantTT:
            return Decimal('0.00')
        # Par défaut on considère 65%, peut être redéfini dans les sous-classes
        return round(self.montantTT * Decimal('0.65'), 2)

    @property
    def total_acteurs(self):
        if not self.montantTT:
            return Decimal('0.00')
        # Par défaut 35%, peut être redéfini dans les sous-classes
        return round(self.montantTT * Decimal('0.35'), 2)

# === Classe spécifique pour Accouchement ===
class Accouchement(BlocOperatoire):
    medecin = models.CharField("Médecin", max_length=255, null=True, blank=True)
    sage_femme = models.CharField("Sage-femme", max_length=255, null=True, blank=True)
    aide = models.CharField("Aide", max_length=255, null=True, blank=True)
    pediatre = models.CharField("Pédiatre", max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Accouchement: {self.libelle} - {self.montantTT} FCFA"

    @property
    def part_medecin(self):
        return round(self.total_acteurs * Decimal('0.4286'), 2)

    @property
    def part_sage_femme(self):
        return round(self.total_acteurs * Decimal('0.2857'), 2)

    @property
    def part_aide(self):
        return round(self.total_acteurs * Decimal('0.1429'), 2)

    @property
    def part_pediatre(self):
        return round(self.total_acteurs * Decimal('0.1429'), 2)


# === Classe spécifique pour Césarienne ===
class Cesarienne(BlocOperatoire):
    chirurgien = models.CharField("Chirurgien", max_length=255, null=True, blank=True)
    anesthesiste = models.CharField("Anesthésiste", max_length=255, null=True, blank=True)
    panseur = models.CharField("Panseur", max_length=255, null=True, blank=True)
    instrumentiste = models.CharField("Instrumentiste", max_length=255, null=True, blank=True)
    aide = models.CharField("Aide", max_length=255, null=True, blank=True)
    pediatre = models.CharField("Pédiatre", max_length=255, null=True, blank=True)
    sage_femme = models.CharField("Sage-femme", max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Césarienne: {self.libelle} - {self.montantTT} FCFA"

    @property
    def part_chirurgien(self):
        return round(self.total_acteurs * Decimal('0.28'), 2)

    @property
    def part_aide(self):
        return round(self.total_acteurs * Decimal('0.15'), 2)

    @property
    def part_anesthesiste(self):
        return round(self.total_acteurs * Decimal('0.21'), 2)

    @property
    def part_panseur(self):
        return round(self.total_acteurs * Decimal('0.10'), 2)

    @property
    def part_instrumentiste(self):
        return round(self.total_acteurs * Decimal('0.10'), 2)

    @property
    def part_pediatre(self):
        return round(self.total_acteurs * Decimal('0.08'), 2)

    @property
    def part_sage_femme(self):
        return round(self.total_acteurs * Decimal('0.08'), 2)


# === Classe spécifique pour Cure de hernie ===
class CureHernie(BlocOperatoire):
    chirurgien = models.CharField("Chirurgien", max_length=255, null=True, blank=True)
    aide = models.CharField("Aide", max_length=255, null=True, blank=True)
    panseur = models.CharField("Panseur", max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Cure de hernie: {self.libelle} - {self.montantTT} FCFA"

    @property
    def maison(self):
        if not self.montantTT:
            return Decimal('0.00')
        # La maison prend 50% ici
        return round(self.montantTT * Decimal('0.50'), 2)

    @property
    def total_acteurs(self):
        if not self.montantTT:
            return Decimal('0.00')
        # Les acteurs prennent aussi 50%
        return round(self.montantTT * Decimal('0.50'), 2)

    @property
    def part_chirurgien(self):
        return round(self.total_acteurs * Decimal('0.80'), 2)

    @property
    def part_aide(self):
        return round(self.total_acteurs * Decimal('0.15'), 2)

    @property
    def part_panseur(self):
        return round(self.total_acteurs * Decimal('0.05'), 2)


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
    
    # Classe Acte Médical (non consultation)
# -----------------------------
from django.db import models
from decimal import Decimal

class ActeTechnique(models.Model):
    TYPE_CHOICES = [
        ('Circoncision', 'Circoncision'),
        ('Bartholinite', 'Bartholinite'),
        ('Catpotomie', 'Catpotomie'),
        ('Cerclage', 'Cerclage'),
        ('SHT', 'SHT'),
        ('SONO', 'SONO'),
        ('IVG', 'IVG'),
    ]

    libelle = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    acteur_nom = models.CharField(max_length=255)
    acteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aide_nom = models.CharField(max_length=255, blank=True, null=True)
    aide_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.libelle}"

    def calcul_repartition(self):
        self.msn_montant = self.montant_total * Decimal('0.70')
        self.acteur_montant = self.montant_total * Decimal('0.25')
        self.aide_montant = self.montant_total * Decimal('0.05')


class Varicocele(models.Model):
    libelle = models.CharField(max_length=255)
    montantTT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    chirurgien = models.CharField(max_length=255)
    aide = models.CharField(max_length=255)
    panseur = models.CharField(max_length=255)

    @property
    def maison(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.50'), 2)
        return Decimal('0.00')

    @property
    def montant_acteurs(self):
        if self.montantTT is not None:
            return round(self.montantTT * Decimal('0.50'), 2)
        return Decimal('0.00')

    @property
    def chirurgien_part(self):
        return round(self.montant_acteurs * Decimal('0.80'), 2)

    @property
    def aide_part(self):
        return round(self.montant_acteurs * Decimal('0.15'), 2)

    @property
    def panseur_part(self):
        return round(self.montant_acteurs * Decimal('0.05'), 2)

    def __str__(self):
        return f"{self.libelle} - {self.montantTT} FCFA"
