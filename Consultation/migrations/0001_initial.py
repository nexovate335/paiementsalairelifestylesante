# Generated by Django 5.1.7 on 2025-07-17 10:20

import Consultation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CertificatMedical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=255)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('msn_nom', models.CharField(max_length=255)),
                ('msn_montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('acteur_nom', models.CharField(max_length=255)),
                ('acteur_montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('generale', 'Consultation Générale'), ('prenatale', 'Consultation Prénatale'), ('pediatrique', 'Consultation Pédiatrique'), ('anesthesique', 'Consultation Anesthésique'), ('orl', 'Consultation ORL')], max_length=20)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('msn_montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('acteur_nom', models.CharField(max_length=255)),
                ('acteur_montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('aide_nom', models.CharField(blank=True, max_length=255, null=True)),
                ('aide_montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            bases=(models.Model, Consultation.models.RepartitionMixin),
        ),
    ]
