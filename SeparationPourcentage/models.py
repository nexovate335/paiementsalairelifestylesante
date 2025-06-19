# separation_pourcentage/models.py
from django.db import models

class SeparationPourcentage(models.Model):
    date_calcul = models.DateField(auto_now_add=True)
    reste_a_payer = models.DecimalField(max_digits=12, decimal_places=2)

    # Répartitions principales
    tresor_gu = models.DecimalField(max_digits=12, decimal_places=2)
    salaire_dg = models.DecimalField(max_digits=12, decimal_places=2)

    # Investissement
    travaux = models.DecimalField(max_digits=12, decimal_places=2)
    pharmacie = models.DecimalField(max_digits=12, decimal_places=2)
    reparation = models.DecimalField(max_digits=12, decimal_places=2)
    labo = models.DecimalField(max_digits=12, decimal_places=2)

    # Administration
    comptable = models.DecimalField(max_digits=12, decimal_places=2)
    chef_personnel = models.DecimalField(max_digits=12, decimal_places=2)
    ag = models.DecimalField(max_digits=12, decimal_places=2)
    surveillant = models.DecimalField(max_digits=12, decimal_places=2)
    informatique = models.DecimalField(max_digits=12, decimal_places=2)

    # Autres services
    reception_1 = models.DecimalField(max_digits=12, decimal_places=2)
    reception_2 = models.DecimalField(max_digits=12, decimal_places=2)
    caisse_1 = models.DecimalField(max_digits=12, decimal_places=2)
    caisse_2 = models.DecimalField(max_digits=12, decimal_places=2)
    cyril = models.DecimalField(max_digits=12, decimal_places=2)
    rosine = models.DecimalField(max_digits=12, decimal_places=2)
    securite_1 = models.DecimalField(max_digits=12, decimal_places=2)
    securite_2 = models.DecimalField(max_digits=12, decimal_places=2)
    securite_3 = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Répartition du {self.date_calcul}"
