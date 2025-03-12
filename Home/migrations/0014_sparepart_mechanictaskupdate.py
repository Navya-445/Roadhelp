# Generated by Django 5.1.2 on 2025-03-10 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0013_alter_customer_mobile_alter_mechanic_mobile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MechanicTaskUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('location_reached_time', models.CharField(blank=True, choices=[('1:00 AM', '1:00 AM'), ('1:00 PM', '1:00 PM'), ('2:00 AM', '2:00 AM'), ('2:00 PM', '2:00 PM'), ('3:00 AM', '3:00 AM'), ('3:00 PM', '3:00 PM'), ('4:00 AM', '4:00 AM'), ('4:00 PM', '4:00 PM'), ('5:00 AM', '5:00 AM'), ('5:00 PM', '5:00 PM'), ('6:00 AM', '6:00 AM'), ('6:00 PM', '6:00 PM'), ('7:00 AM', '7:00 AM'), ('7:00 PM', '7:00 PM'), ('8:00 AM', '8:00 AM'), ('8:00 PM', '8:00 PM'), ('9:00 AM', '9:00 AM'), ('9:00 PM', '9:00 PM'), ('10:00 AM', '10:00 AM'), ('10:00 PM', '10:00 PM'), ('11:00 AM', '11:00 AM'), ('11:00 PM', '11:00 PM'), ('12:00 AM', '12:00 AM'), ('12:00 PM', '12:00 PM')], max_length=10, null=True)),
                ('service_completed_time', models.CharField(blank=True, choices=[('1:00 AM', '1:00 AM'), ('1:00 PM', '1:00 PM'), ('2:00 AM', '2:00 AM'), ('2:00 PM', '2:00 PM'), ('3:00 AM', '3:00 AM'), ('3:00 PM', '3:00 PM'), ('4:00 AM', '4:00 AM'), ('4:00 PM', '4:00 PM'), ('5:00 AM', '5:00 AM'), ('5:00 PM', '5:00 PM'), ('6:00 AM', '6:00 AM'), ('6:00 PM', '6:00 PM'), ('7:00 AM', '7:00 AM'), ('7:00 PM', '7:00 PM'), ('8:00 AM', '8:00 AM'), ('8:00 PM', '8:00 PM'), ('9:00 AM', '9:00 AM'), ('9:00 PM', '9:00 PM'), ('10:00 AM', '10:00 AM'), ('10:00 PM', '10:00 PM'), ('11:00 AM', '11:00 AM'), ('11:00 PM', '11:00 PM'), ('12:00 AM', '12:00 AM'), ('12:00 PM', '12:00 PM')], max_length=10, null=True)),
                ('before_service_picture', models.ImageField(blank=True, null=True, upload_to='service_pics/')),
                ('after_service_picture', models.ImageField(blank=True, null=True, upload_to='service_pics/')),
                ('mechanic_notes', models.TextField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_updates', to='Home.taskassignment')),
                ('spare_parts_used', models.ManyToManyField(blank=True, to='Home.sparepart')),
            ],
        ),
    ]
