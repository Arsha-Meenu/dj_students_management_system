# Generated by Django 4.1.5 on 2023-03-06 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_academics_faculties_session_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='period',
        ),
    ]
