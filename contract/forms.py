from datetime import date
import re
from django import forms
from .models import Contract
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'gouvernorat': forms.Select(attrs={'class': 'form-control', 'id': 'id_gouvernorat', 'required': True}),
            'delegation': forms.Select(attrs={'class': 'form-control', 'id': 'id_delegation', 'required': True}),
            'localite': forms.Select(attrs={'class': 'form-control', 'id': 'id_localite', 'required': True}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_code_postal', 'readonly': 'readonly'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'type_abonnement': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'type_smart_rapido': forms.Select(attrs={'class': 'form-control','required': True}),
            'type_smart_fibre': forms.Select(attrs={'class': 'form-control','required': True}),
            'type_smart_adsl':forms.Select(attrs={'class': 'form-control','required': True}),
            'telephone_contact': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'gsm_contact': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'adresse_installation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'coordonnees': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'cin_recto': forms.FileInput(attrs={'class': 'custom-file-input','required': True}),
            'cin_verso': forms.FileInput(attrs={'class': 'custom-file-input','required': True}),
            'contrat_tt': forms.FileInput(attrs={'class': 'custom-file-input','required': True}),
            'contrat_topnet': forms.FileInput(attrs={'class': 'custom-file-input','required': True}),
            'contrat_general_vente': forms.FileInput(attrs={'class': 'custom-file-input','required': True}),
            'frequence_paiement': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date_naissance': DateInput(attrs={'class': 'form-control', 'type': 'date','required': True}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not re.match("^[a-zA-Zéèêëàâäîïôöûüç-]+$", nom):
            raise ValidationError('Le nom contient des caractères invalides.')
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom')
        if not re.match("^[a-zA-Zéèêëàâäîïôöûüç-]+$", prenom):
            raise ValidationError('Le prénom contient des caractères invalides.')
        return prenom

    

    # def clean_date_naissance(self):
    #     date_naissance = self.cleaned_data.get('date_naissance')
    #     if date_naissance.year > date.today().year - 18:
    #         raise ValidationError("Vous devez avoir au moins 18 ans.")
    #     return date_naissance

    def clean_telephone_contact(self):
        telephone_contact = self.cleaned_data.get('telephone_contact')
        if not re.match(r'^\d{8}$', telephone_contact):
            raise ValidationError('Le numéro de téléphone doit contenir exactement 8 chiffres.')
        return telephone_contact

    def clean_gsm_contact(self):
        gsm_contact = self.cleaned_data.get('gsm_contact')
        if not re.match(r'^\d{8}$', gsm_contact):
            raise ValidationError('Le numéro de GSM doit contenir exactement 8 chiffres.')
        return gsm_contact
    def clean_gsm_contact_2(self):
        gsm_contact_2 = self.cleaned_data.get('gsm_contact_2')
        if gsm_contact_2 and not re.match(r'^\d{8}$', gsm_contact_2):
            raise ValidationError('Le numéro de GSM doit contenir exactement 8 chiffres.')
        return gsm_contact_2

    def clean_numero_piece_identite(self):
        type_piece_identite = self.cleaned_data.get('type_piece_identite')
        numero_piece_identite = self.cleaned_data.get('numero_piece_identite')
        if type_piece_identite == 'CIN' and not re.match(r'^\d{8}$', numero_piece_identite):
            raise ValidationError('Le numéro de CIN doit contenir exactement 8 chiffres.')
        elif type_piece_identite == 'Passport' and not re.match(r'^[a-zA-Z]\d{6}$', numero_piece_identite):
            raise ValidationError('Le numéro de Passport doit contenir une lettre suivie de 6 chiffres.')
        return numero_piece_identite
    

    def clean_coordonnees(self):
        coordonnees = self.cleaned_data.get('coordonnees')
        if coordonnees and not re.match(r"^\d+\.\d+,\d+\.\d+$", coordonnees):
            raise ValidationError('Les coordonnées doivent être au format "10.12502,36.82574".')
        return coordonnees

    def clean(self):
        cleaned_data = super().clean()
        fichiers = ['cin_recto', 'cin_verso', 'contrat_tt', 'contrat_topnet', 'contrat_general_vente']
        for fichier in fichiers:
            file = cleaned_data.get(fichier)
            if file and not file.name.endswith(('.jpg', '.png', '.pdf')):
                self.add_error(fichier, 'Le fichier doit être au format jpg, png ou pdf.')
        return cleaned_data