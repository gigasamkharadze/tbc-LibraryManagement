# Generated by Django 5.0.6 on 2024-05-17 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_birth_date_alter_user_personal_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(verbose_name='birth date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='personal_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='personal number'),
        ),
    ]
