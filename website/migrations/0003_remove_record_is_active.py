# Generated by Django 4.2.9 on 2024-01-17 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_record_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='is_active',
        ),
    ]