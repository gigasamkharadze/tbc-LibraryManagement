# Generated by Django 5.0.6 on 2024-05-16 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_checkout_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='checkout_date',
            field=models.DateField(verbose_name='checkout date'),
        ),
    ]