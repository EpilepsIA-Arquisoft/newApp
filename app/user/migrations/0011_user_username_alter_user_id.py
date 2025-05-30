# Generated by Django 5.2.1 on 2025-05-17 21:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_is_superuser_alter_user_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=None, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
