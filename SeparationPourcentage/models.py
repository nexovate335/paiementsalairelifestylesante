from django.db import models
from django.utils import timezone, formats
from decimal import Decimal
from datetime import datetime

# Choix des mois en français
MOIS_CHOICES = [
    (1, "janvier"), (2, "février"), (3, "mars"), (4, "avril"),
    (5, "mai"), (6, "juin"), (7, "juillet"), (8, "août"),
    (9, "septembre"), (10, "octobre"), (11, "novembre"), (12, "décembre")
]

ANNEE_CHOICES = [(annee, str(annee)) for annee in range(2020, 2036)]

class SeparationPourcentage(models.Model):
    date_calcul = models.DateField(auto_now_add=True)
    mois = models.IntegerField(choices=MOIS_CHOICES, null=True, blank=True)
    annee = models.IntegerField(choices=ANNEE_CHOICES, null=True, blank=True)

    reste_a_payer = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Répartitions principales
    tresor_gu = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salaire_dg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Investissement
    travaux = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pharmacie = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reparation = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    labo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Administration
    comptable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    chef_personnel = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ag = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    surveillant = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    informatique = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Autres services
    reception_1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reception_2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    caisse_1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    caisse_2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cyril = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rosine = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    securite_1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    securite_2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    securite_3 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def mois_formate(self):
        if self.mois and self.annee:
            dt = datetime(year=self.annee, month=self.mois, day=1)
            return formats.date_format(dt, "F Y")
        return "Mois non défini"

    def __str__(self):
        return f"Répartition du {self.mois_formate()}"

    class Meta:
        verbose_name = "Répartition Mensuelle"
        verbose_name_plural = "Répartitions Mensuelles"
