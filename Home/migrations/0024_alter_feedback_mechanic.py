# Generated by Django 5.1.2 on 2025-03-24 05:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0023_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.mechanicprofile'),
        ),
    ]
