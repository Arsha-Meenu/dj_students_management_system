# Generated by Django 4.1.5 on 2023-03-13 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_remove_subjects_teache'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.teacher'),
        ),
    ]
