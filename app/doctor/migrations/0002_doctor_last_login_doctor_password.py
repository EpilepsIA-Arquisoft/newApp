# Generated by Django 5.2.1 on 2025-05-12 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='password',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
