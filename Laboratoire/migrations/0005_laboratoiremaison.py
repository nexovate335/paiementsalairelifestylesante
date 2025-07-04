# Generated by Django 5.1.1 on 2025-06-28 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Laboratoire', '0004_rename_msn_30_tarif_trios_labotrios_msn_part_tarif_trios'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaboratoireMaison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('msn_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('acteurs_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('prescripteur_nom', models.CharField(max_length=100)),
                ('prescripteur_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('technicien_nom', models.CharField(max_length=100)),
                ('technicien_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('preleveur_nom', models.CharField(max_length=100)),
                ('preleveur_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('assistante_nom', models.CharField(max_length=100)),
                ('assistante_part', models.DecimalField(decimal_places=2, editable=False, max_digits=12)),
                ('mois', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=6)),
                ('annee', models.IntegerField(default=2025)),
            ],
            options={
                'verbose_name': 'Laboratoire Maison',
                'verbose_name_plural': 'Laboratoires Maison',
                'ordering': ['-annee', '-mois'],
            },
        ),
    ]
