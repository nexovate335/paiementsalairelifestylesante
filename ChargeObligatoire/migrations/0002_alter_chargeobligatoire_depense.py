# Generated by Django 5.2.1 on 2025-06-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChargeObligatoire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargeobligatoire',
            name='depense',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
