# Generated by Django 5.2.1 on 2025-07-18 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bulletin_laboratoire', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fichedepaie',
            old_name='autres_prestations',
            new_name='prime_hospitalisation',
        ),
    ]
