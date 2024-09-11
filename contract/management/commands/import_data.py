import pandas as pd
from django.core.management.base import BaseCommand
from contract.models import Gouvernorat, Delegation, Localite, CodePostal

class Command(BaseCommand):
    help = 'Importe les données de codes postaux à partir d\'un fichier Excel'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\LENOVO\Downloads\codes_tunisie.xlsx'
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            gouvernorat, _ = Gouvernorat.objects.get_or_create(nomGouvernorat=row['nomGouvernorat'])
            delegation, _ = Delegation.objects.get_or_create(nomDelegation=row['nomDelegation'], gouvernorat=gouvernorat)
            localite, _ = Localite.objects.get_or_create(nomLocalite=row['nomLocalite'], delegation=delegation)
            CodePostal.objects.get_or_create(localite=localite, codePostal=row['codePostal'])

        self.stdout.write(self.style.SUCCESS('Les données de codes postaux ont été importées avec succès.'))
