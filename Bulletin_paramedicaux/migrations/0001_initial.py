# Generated by Django 5.2.1 on 2025-06-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrestationMensuelle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('poste', models.CharField(blank=True, max_length=100, null=True)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('fonction', models.CharField(blank=True, max_length=100, null=True)),
                ('mois', models.CharField(blank=True, choices=[('janvier', 'Janvier'), ('fevrier', 'Février'), ('mars', 'Mars'), ('avril', 'Avril'), ('mai', 'Mai'), ('juin', 'Juin'), ('juillet', 'Juillet'), ('aout', 'Août'), ('septembre', 'Septembre'), ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('decembre', 'Décembre')], max_length=10, null=True)),
                ('annee', models.CharField(blank=True, choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], default='2025', max_length=4, null=True)),
                ('consultations_urgences', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pharmacie_bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prescriptions', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pensements', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pharmacie_nuit_weekend', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('laboratoire_nuit_weekend', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('aides_aux_actes', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prescriptions_laboratoire', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prime_caisse', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prescription_echo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('anesthesie', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prime_transport', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('anciennete', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('avance_salaire', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('observation', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
