# Generated by Django 5.2.1 on 2025-05-11 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0002_paciente_edad_paciente_sexo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='sexo',
        ),
    ]
