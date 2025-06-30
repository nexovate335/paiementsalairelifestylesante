# models.py
from django.db import models
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from .pourcentages_reels import POURCENTAGES

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
        return f"{self.nom_personne} - {self.fonction} - {self.designation} - {self.mois}/{self.annee}"

    def calcul_pourcentage_et_gain(self):
        designation_cle = (self.designation or '').upper().strip()
        fonction_cle = (self.fonction or '').lower().replace('é', 'e').replace(' ', '_')

        repartition = POURCENTAGES.get(designation_cle, {})

        if not repartition:
            # Désignation non trouvée -> pas de gain
            self.pourcentage = Decimal(0)
            self.montant_total = Decimal(self.montant) * self.nombre
            self.gain = Decimal(0)
            return

        # Montant total calculé une seule fois
        self.montant_total = Decimal(self.montant) * self.nombre

        # 1. Cas avec 'maison' + 'sous_repartition' (le plus courant)
        if 'maison' in repartition and 'sous_repartition' in repartition:
            maison_percent = Decimal(repartition['maison'])
            if fonction_cle == 'maison':
                self.pourcentage = maison_percent
            else:
                reste = Decimal(100) - maison_percent
                sous_repartition = repartition['sous_repartition']
                if fonction_cle in sous_repartition:
                    proportion = Decimal(sous_repartition[fonction_cle])
                    # calcul proportionnel du reste
                    self.pourcentage = (reste * proportion / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    self.pourcentage = Decimal(0)

        # 2. Cas avec 'maison' + 'acteurs_global' + 'sous_repartition'
        elif 'maison' in repartition and 'acteurs_global' in repartition and 'sous_repartition' in repartition:
            maison_percent = Decimal(repartition['maison'])
            acteurs_global = Decimal(repartition['acteurs_global'])
            if fonction_cle == 'maison':
                self.pourcentage = maison_percent
            else:
                sous_repartition = repartition['sous_repartition']
                if fonction_cle in sous_repartition:
                    proportion = Decimal(sous_repartition[fonction_cle])
                    self.pourcentage = (acteurs_global * proportion / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    self.pourcentage = Decimal(0)

        # 3. Cas simple avec 'maison' + 'acteur' + éventuellement 'aide'
        elif 'maison' in repartition and 'acteur' in repartition:
            if fonction_cle == 'maison':
                self.pourcentage = Decimal(repartition['maison'])
            elif fonction_cle == 'acteur':
                self.pourcentage = Decimal(repartition['acteur'])
            elif fonction_cle == 'aide' and 'aide' in repartition:
                self.pourcentage = Decimal(repartition['aide'])
            else:
                self.pourcentage = Decimal(0)

        # 4. Cas où seulement 'maison' est défini (ex: sans acteurs)
        elif 'maison' in repartition:
            if fonction_cle == 'maison':
                self.pourcentage = Decimal(repartition['maison'])
            else:
                self.pourcentage = Decimal(0)

        else:
            # Pas de correspondance = 0%
            self.pourcentage = Decimal(0)

        # Calcul final du gain
        self.gain = (self.montant_total * self.pourcentage / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class DocteurSalaire(SalaireBase):
    def save(self, *args, **kwargs):
        self.calcul_pourcentage_et_gain()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Salaire Docteur"
        verbose_name_plural = "Salaires Docteurs"
        ordering = ['-annee', '-mois']


class ParaMedicoSalaire(SalaireBase):
    def save(self, *args, **kwargs):
        self.calcul_pourcentage_et_gain()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Salaire Paramédico"
        verbose_name_plural = "Salaires Paramédicaux"
        ordering = ['-annee', '-mois']


class PreleveurSalaire(SalaireBase):
    def save(self, *args, **kwargs):
        self.montant_total = Decimal(self.montant) * self.nombre
        self.pourcentage = Decimal(15)  # fixe 15%
        self.gain = (self.montant_total * self.pourcentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Salaire Prélèveur"
        verbose_name_plural = "Salaires Prélèveurs"
        ordering = ['-annee', '-mois']


class PratiqueurSalaire(SalaireBase):
    def save(self, *args, **kwargs):
        self.montant_total = Decimal(self.montant) * self.nombre
        self.pourcentage = Decimal(45)  # fixe 45%
        self.gain = (self.montant_total * self.pourcentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Salaire Pratiqueur"
        verbose_name_plural = "Salaires Pratiqueurs"
        ordering = ['-annee', '-mois']


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
        return (self.arrivee_true or 0) * (self.montant or 0)

    def __str__(self):
        return f"{self.nom_personne} - {self.fonction} - {self.mois}/{self.annee}"

    class Meta:
        verbose_name = "Prime de Transport"
        verbose_name_plural = "Primes de Transport"
        ordering = ['-annee', '-mois']
