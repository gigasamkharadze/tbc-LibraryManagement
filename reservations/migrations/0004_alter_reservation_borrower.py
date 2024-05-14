# Generated by Django 5.0.6 on 2024-05-14 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_alter_reservation_book'),
        ('users', '0002_alter_user_birth_date_alter_user_personal_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='users.borrower', verbose_name='Borrower'),
        ),
    ]