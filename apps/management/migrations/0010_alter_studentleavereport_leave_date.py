# Generated by Django 4.1.5 on 2023-01-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_admissionyear_attendance_studentleavereport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentleavereport',
            name='leave_date',
            field=models.DateField(),
        ),
    ]