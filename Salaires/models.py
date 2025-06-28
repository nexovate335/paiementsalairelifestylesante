from django.db import models
from datetime import date
from decimal import Decimal

MOIS_CHOICES = [(i, date(1900, i, 1).strftime('%B')) for i in range(1, 13)]


class SalaireBase(models.Model):
    MOIS_CHOICES = MOIS_CHOICES
    nom_personne = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nombre = models.PositiveIntegerField(default=0)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)
    gain = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    mois = models.IntegerField(choices=MOIS_CHOICES, default=date.today().month)
    annee = models.IntegerField(default=date.today().year)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nom_personne} - {self.fonction} - {self.mois}/{self.annee}"


# ✅ DocteurSalaire (25% fixe)
class DocteurSalaire(SalaireBase):
    nombre_service = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "Salaire Docteur"
        verbose_name_plural = "Salaires Docteurs"
        ordering = ['-annee', '-mois']

    def save(self, *args, **kwargs):
        self.nombre_service = self.nombre
        self.montant_total = self.montant * self.nombre_service
        self.pourcentage = Decimal(25)
        self.gain = (self.montant_total * self.pourcentage) / 100
        super().save(*args, **kwargs)


# ✅ ParaMedicoSalaire (Pourcentage par désignation)
class ParaMedicoSalaire(SalaireBase):
    class Meta:
        verbose_name = "Salaire Paramédico"
        verbose_name_plural = "Salaires Paramédicaux"
        ordering = ['-annee', '-mois']

    def save(self, *args, **kwargs):
        pourcentages = {
            'PST': 25,
            'Biopsie': 25,
            'Dechirure': 25,
            'Accouchement': 14,
            'Ventouse': 25,
            'Refection': 25,
            'Sono': 20,
            'Assistante_CNS': 5,
            'Echo_D': 5,
            'Prime garde': 1,
            'T3G': 25,
            'Hernie': 8,
            'Varicocele': 8,
            'Myomectomie': 10,
            'HERNIE OMBLICALE': 10,
        }

        self.pourcentage = Decimal(pourcentages.get(self.designation, 0))
        self.montant_total = self.montant * self.nombre
        self.gain = (self.montant_total * self.pourcentage) / 100
        super().save(*args, **kwargs)


# ✅ PreleveurSalaire (15% fixe)
class PreleveurSalaire(SalaireBase):
    class Meta:
        verbose_name = "Salaire Prélèveur"
        verbose_name_plural = "Salaires Prélèveurs"
        ordering = ['-annee', '-mois']

    def save(self, *args, **kwargs):
        self.montant_total = self.montant * self.nombre
        self.pourcentage = Decimal(15)
        self.gain = (self.montant_total * self.pourcentage) / 100
        super().save(*args, **kwargs)


# ✅ PratiqueurSalaire (45% fixe)
class PratiqueurSalaire(SalaireBase):
    class Meta:
        verbose_name = "Salaire Pratiqueur"
        verbose_name_plural = "Salaires Pratiqueurs"
        ordering = ['-annee', '-mois']

    def save(self, *args, **kwargs):
        self.montant_total = self.montant * self.nombre
        self.pourcentage = Decimal(45)
        self.gain = (self.montant_total * self.pourcentage) / 100
        super().save(*args, **kwargs)


# ✅ PrimeTransport
class PrimeTransport(models.Model):
    MOIS_CHOICES = MOIS_CHOICES
    nom_personne = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    nombre_total = models.PositiveIntegerField()
    arrivee_true = models.PositiveIntegerField()
    arrivee_false = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.IntegerField(choices=MOIS_CHOICES, default=date.today().month)
    annee = models.IntegerField(default=date.today().year)

    def prime_totale(self):
        if self.arrivee_true is not None and self.montant is not None:
            return self.arrivee_true * self.montant
        return Decimal('0.00')

    prime_totale.short_description = "Montant Prime Transport"

    def __str__(self):
        return f"{self.nom_personne} - {self.fonction} - {self.mois}/{self.annee}"

    class Meta:
        verbose_name = "Prime de Transport"
        verbose_name_plural = "Primes de Transport"
        ordering = ['-annee', '-mois']
