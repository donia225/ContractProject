# Generated by Django 5.0.7 on 2024-07-20 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0012_codepostal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codepostal',
            name='code_postal',
        ),
        migrations.RemoveField(
            model_name='codepostal',
            name='delegation',
        ),
        migrations.RemoveField(
            model_name='codepostal',
            name='gouvernorat',
        ),
        migrations.RemoveField(
            model_name='delegation',
            name='codeDelegation',
        ),
        migrations.RemoveField(
            model_name='gouvernorat',
            name='codeGouvernorat',
        ),
        migrations.RemoveField(
            model_name='localite',
            name='codeLocalite',
        ),
        migrations.AddField(
            model_name='codepostal',
            name='codePostal',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='codepostal',
            name='localite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.localite'),
        ),
        migrations.AlterField(
            model_name='gouvernorat',
            name='nomGouvernorat',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
