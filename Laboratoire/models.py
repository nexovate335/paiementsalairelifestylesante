from django.db import models
from decimal import Decimal
from datetime import date
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



class LaboTrios(models.Model):
    libelle = models.CharField(max_length=255)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    tarif_maison = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_trios = models.DecimalField(max_digits=10, decimal_places=2)

    # Résultats de calcul
    benefice_maison = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    msn_part_tarif_trios = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    total_g = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    msn_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    acteurs_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    preleveur_nom = models.CharField(max_length=255)
    preleveur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    prescripteur_nom = models.CharField(max_length=255)
    prescripteur_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        # Bénéfice maison = tarif maison – tarif trios
        self.benefice_maison = self.tarif_maison - self.tarif_trios

        # MSN prend 30% du tarif trios
        self.msn_part_tarif_trios = self.tarif_trios * Decimal('0.30')

        # Total G = bénéfice maison + MSN 30% tarif trios
        self.total_g = self.benefice_maison + self.msn_part_tarif_trios

        # Répartition du total G : 80% MSN, 20% acteurs
        self.msn_final = self.total_g * Decimal('0.80')
        self.acteurs_total = self.total_g * Decimal('0.20')

        # Répartition des 20% acteurs : 40% préleveur, 60% prescripteur
        self.preleveur_montant = self.acteurs_total * Decimal('0.40')
        self.prescripteur_montant = self.acteurs_total * Decimal('0.60')

    def save(self, *args, **kwargs):
        self.calcul_repartition()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Labo Trios - {self.libelle}"


class LaboratoireMaison(models.Model):
    libelle = models.CharField(max_length=100)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)

    # Calcul automatique
    msn_part = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    acteurs_part = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    prescripteur_nom = models.CharField(max_length=100)
    prescripteur_gain = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    technicien_nom = models.CharField(max_length=100)
    technicien_gain = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    preleveur_nom = models.CharField(max_length=100)
    preleveur_gain = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    assistante_nom = models.CharField(max_length=100)
    assistante_gain = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    mois = models.CharField(max_length=10, choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.CharField(max_length=4, choices=ANNEE_CHOICES, default='2025', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Répartition
        self.msn_part = self.montant_total * Decimal('0.80')
        self.acteurs_part = self.montant_total * Decimal('0.20')

        self.prescripteur_gain = self.acteurs_part * Decimal('0.30')
        self.technicien_gain = self.acteurs_part * Decimal('0.45')
        self.preleveur_gain = self.acteurs_part * Decimal('0.15')
        self.assistante_gain = self.acteurs_part * Decimal('0.10')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle} - {self.mois}/{self.annee}"

    class Meta:
        verbose_name = "Laboratoire Maison"
        verbose_name_plural = "Laboratoires Maison"
        ordering = ['-annee', '-mois']
