# Generated by Django 5.0.3 on 2024-05-18 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='school_years',
            new_name='classes',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='modules',
            new_name='courses',
        ),
    ]