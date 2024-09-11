from django.db import models
from django.contrib.auth.models import User

class Gouvernorat(models.Model):
    nomGouvernorat = models.CharField(max_length=100, unique=True,null=True)

    def __str__(self):
        return self.nomGouvernorat

class Delegation(models.Model):
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE)
    nomDelegation = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.nomDelegation

class Localite(models.Model):
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    nomLocalite = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.nomLocalite

class CodePostal(models.Model):
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    codePostal = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.codePostal
class Contract(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.created_by is None:
            raise ValueError("Le champ 'created_by' ne peut pas être vide.")
        super().save(*args, **kwargs)
    TYPE_ABONNEMENT_CHOICES = [
        ('SMART ADSL', 'SMART ADSL'),
        ('VDSL', 'VDSL'),
        ('SMART FIBRE', 'SMART FIBRE'),
        ('SMART RAPIDO', 'SMART RAPIDO')
    ]
    SMART_ADSL= [
        ('SMART ADSL 10M','SMART ADSL 10M'),
        ('SMART ADSL 12M','SMART ADSL 12M'),
        ('SMART ADSL 20M','SMART ADSL 20M'),
    ]
    SMART_RAPIDO_CHOICES = [
        ('SMART Rapido 20M GU TOPNET', 'SMART Rapido 20M GU TOPNET'),
        ('SMART Rapido 30M GU TOPNET', 'SMART Rapido 30M GU TOPNET'),
        ('SMART Rapido 50M GU TOPNET', 'SMART Rapido 50M GU TOPNET'),
        ('SMART Rapido 100M GU TOPNET', 'SMART Rapido 100M GU TOPNET'),
        ('SMART RAPIDO 20M (sans voix)', 'SMART RAPIDO 20M (sans voix)'),
        ('SMART RAPIDO 30M (sans voix)', 'SMART RAPIDO 30M (sans voix)'),
        ('SMART RAPIDO 50M (sans voix)', 'SMART RAPIDO 50M (sans voix)'),
        ('SMART RAPIDO 100M (sans voix)', 'SMART RAPIDO 100M (sans voix)'),
        ('PROMO SMART RAPIDO 20M (Sans Voix)', 'PROMO SMART RAPIDO 20M (Sans Voix)'),
        ('PROMO SMART RAPIDO 30M (Sans Voix)', 'PROMO SMART RAPIDO 30M (Sans Voix)'),
        ('PROMO SMART RAPIDO 50M (Sans Voix)', 'PROMO SMART RAPIDO 50M (Sans Voix)'),
        ('PROMO SMART RAPIDO 100M (Sans Voix)', 'PROMO SMART RAPIDO 100M (Sans Voix)'),
        ('Fidélité SMART RAPIDO 50M (sans voix)', 'Fidélité SMART RAPIDO 50M (sans voix)')
    ]
    SMART_FIBRE = [
        ('20M', '20M'),
        ('50M', '50M'),
        ('100M', '100M'),
    ]

    FREQUENCE_PAIEMENT_CHOICES = [
        ('1', '1 mois'),
        ('3', '3 mois'),
        ('6', '6 mois'),
        ('12', '12 mois'),
    ]
    CIVILITE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Mlle', 'Mlle'),
    ]

    type_abonnement = models.CharField(max_length=100, choices=TYPE_ABONNEMENT_CHOICES)
    type_smart_rapido = models.CharField(max_length=100, choices=SMART_RAPIDO_CHOICES, blank=True, null=True)
    type_smart_fibre = models.CharField(max_length=100, choices=SMART_FIBRE, blank=True, null=True)
    type_smart_adsl = models.CharField(max_length=100, choices=SMART_ADSL,blank=True, null=True)
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    civilite = models.CharField(max_length=4, choices=CIVILITE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    TYPE_PIECE_CHOICES = [
        ('CIN', 'CIN'),
        ('Passport', 'Passport'),
    ]
    type_piece_identite = models.CharField(max_length=20, choices=TYPE_PIECE_CHOICES)
    numero_piece_identite = models.CharField(max_length=50)
    telephone_contact = models.CharField(max_length=20)
    gsm_contact = models.CharField(max_length=20)
    gsm_contact_2 = models.CharField(max_length=20, blank=True, null=True)
    adresse_installation = models.TextField()
    coordonnees = models.CharField(max_length=255, blank=True, null=True)
    cin_recto = models.FileField(max_length=255, blank=True, null=True)
    cin_verso = models.FileField(max_length=255, blank=True, null=True)
    contrat_tt = models.FileField(max_length=255, blank=True, null=True)
    contrat_topnet = models.FileField(max_length=255, blank=True, null=True)
    contrat_general_vente = models.FileField(max_length=255, blank=True, null=True)
    frequence_paiement = models.CharField(max_length=2, choices=FREQUENCE_PAIEMENT_CHOICES)

    def __str__(self):
        return f'{self.nom} {self.prenom} - {self.numero_piece_identite}'
