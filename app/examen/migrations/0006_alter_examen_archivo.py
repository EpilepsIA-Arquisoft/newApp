# Generated by Django 5.2.1 on 2025-05-11 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examen', '0005_alter_examen_archivo_alter_examen_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='archivo',
            field=models.FileField(default=None, upload_to='examenes_temp/'),
        ),
    ]
