# Generated by Django 4.1.5 on 2023-03-13 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0038_subjects_teacher'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subjects',
            new_name='Subject',
        ),
    ]
