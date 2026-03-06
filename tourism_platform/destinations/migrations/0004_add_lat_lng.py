"""Add latitude and longitude fields to Destination

Generated manually.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0003_homevideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
