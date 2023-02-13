# Generated by Django 4.1.5 on 2023-02-13 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profiles',
            field=models.FileField(null=True, upload_to='profiles', validators=[django.core.validators.FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp'])], verbose_name='user profile'),
        ),
    ]
