# Generated by Django 5.0.3 on 2024-06-06 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
