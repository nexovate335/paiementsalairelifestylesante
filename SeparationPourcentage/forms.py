# separation_pourcentage/forms.py
from django import forms
from .models import SeparationPourcentage
from ChargeObligatoire.models import TraitementChargeObligatoire

class SeparationPourcentageForm(forms.ModelForm):
    class Meta:
        model = SeparationPourcentage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            reste = TraitementChargeObligatoire.calculer_reste()

            # On vérifie que le champ existe avant d’y accéder
            if 'reste_a_payer' in self.fields:
                self.fields['reste_a_payer'].initial = reste
            if 'tresor_gu' in self.fields:
                self.fields['tresor_gu'].initial = reste * 0.25
            if 'salaire_dg' in self.fields:
                self.fields['salaire_dg'].initial = reste * 0.10

            # Investissement
            investissement = reste * 0.50 / 4
            for field in ['travaux', 'pharmacie', 'reparation', 'labo']:
                if field in self.fields:
                    self.fields[field].initial = investissement

            # Administration
            admin_total = reste * 0.15 * 0.40
            initial_admin = {
                'comptable': admin_total * 0.30,
                'chef_personnel': admin_total * 0.16,
                'ag': admin_total * 0.20,
                'surveillant': admin_total * 0.20,
                'informatique': admin_total * 0.12,
            }
            for field, value in initial_admin.items():
                if field in self.fields:
                    self.fields[field].initial = value

            # Autres services
            autre_total = reste * 0.15 * 0.60
            other_fields = {
                'reception_1': autre_total * 0.25 / 2,
                'reception_2': autre_total * 0.25 / 2,
                'caisse_1': autre_total * 0.25 / 2,
                'caisse_2': autre_total * 0.25 / 2,
                'cyril': autre_total * 0.25 * 0.16,
                'rosine': autre_total * 0.25 * 0.09,
                'securite_1': autre_total * 0.25 / 3,
                'securite_2': autre_total * 0.25 / 3,
                'securite_3': autre_total * 0.25 / 3,
            }
            for field, value in other_fields.items():
                if field in self.fields:
                    self.fields[field].initial = value

        except Exception as e:
            # Log l'erreur en console au lieu de planter
            print("Erreur dans le formulaire SeparationPourcentageForm :", e)
