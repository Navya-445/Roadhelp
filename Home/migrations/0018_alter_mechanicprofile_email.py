# Generated by Django 5.1.2 on 2025-03-21 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0017_alter_mechanicprofile_aadhar_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mechanicprofile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
