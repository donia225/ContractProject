# Generated by Django 5.0.7 on 2024-08-29 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0016_alter_contract_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='created_by',
        ),
    ]
