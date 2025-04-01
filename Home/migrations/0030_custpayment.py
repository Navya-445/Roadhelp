# Generated by Django 5.1.2 on 2025-04-01 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0029_paymentinfo_is_paid_paymentinfo_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_request_name', models.CharField(max_length=255)),
                ('cust_name', models.CharField(max_length=255)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
    ]
