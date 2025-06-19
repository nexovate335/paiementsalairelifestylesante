from django.db import models
from decimal import Decimal

class LaboTrios(models.Model):
    libelle = models.CharField(max_length=255)

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
