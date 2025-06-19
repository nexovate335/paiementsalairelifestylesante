from django.db import models
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP

# === Paiements simples ===

class PaiementHospitalisation(models.Model):
    libelle = models.CharField(max_length=255)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    msn_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def calcul_repartition(self):
        montant = self.montant_total or Decimal('0.00')
        self.msn_montant = montant * Decimal('0.65')

        acteurs = self.acteurhospitalisation_set.all()
        nb_acteurs = acteurs.count()

        if nb_acteurs > 0:
            part_individuelle = (montant * Decimal('0.35')) / nb_acteurs
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


