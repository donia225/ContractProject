import calendar
import json
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import pandas as pd

import contract
from .models import CodePostal, Delegation, Localite, Contract
from .forms import ContractForm
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from bs4 import BeautifulSoup
import logging
from django.db.models import Count
from django.db.models.functions import ExtractYear
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Contract
from urllib.parse import quote


@login_required
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.created_by = request.user  # Assigner l'utilisateur connecté
            if not request.user.is_staff:  # Si l'utilisateur est un revendeur
                contract.status = 'pending'  # Définir le statut par défaut pour le revendeur
            contract.save()
            return redirect('list_contract')
    else:
        form = ContractForm(user=request.user)
    
    return render(request, 'contract/add_contract.html', {'form': form})


@login_required
def list_contract(request):
    print(f"User: {request.user}, Is staff: {request.user.is_staff}")

    search_query = request.GET.get('search', '')

    if request.user.is_staff:  # Si l'utilisateur est un administrateur
        contracts = Contract.objects.exclude(status='rejected')  # Voir tous les contrats sauf ceux rejetés
    else:  # Si l'utilisateur est un revendeur
        contracts = Contract.objects.filter(created_by=request.user)  # Voir seulement les contrats qu'il a créés

    # Si le champ de recherche n'est pas vide, appliquer le filtre
    if search_query:
        contracts = contracts.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(localite__nomLocalite__icontains=search_query) |
            Q(gouvernorat__nomGouvernorat__icontains=search_query) |
            Q(delegation__nomDelegation__icontains=search_query)
        )
    
    print(contracts.query)
    return render(request, 'contract/list_contract.html', {'contracts': contracts, 'search_query': search_query})




@login_required
def edit_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)

    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract, user=request.user)  # Passer user ici aussi
        if form.is_valid():
            # S'assurer que le champ created_by n'est pas vide
            if contract.created_by is None:
                contract.created_by = request.user
          
            form.save()
            return redirect('list_contract')
    else:
        form = ContractForm(instance=contract, user=request.user)  # Passer user ici aussi

    return render(request, 'contract/edit_contract.html', {'form': form, 'contract': contract})


@never_cache
@login_required
def details_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contract/details_contract.html', {'contract': contract})


@never_cache
@login_required
def test_view(request):
    file_path = r'C:\Users\LENOVO\Downloads\codes_tunisie.xlsx'
    df = pd.read_excel(file_path)

    nomGouvernorat = 'ARIANA'
    nomDelegation = 'RAOUED'

    delegations_from_gouvernorat = get_delegations_by_gouvernorat(df, nomGouvernorat)
    localites_from_delegation = get_secteurs_by_delegation(df, nomDelegation)
    all_gouvernorats = get_all_gouvernorats(df)

    return JsonResponse({
        "delegations_from_gouvernorat": delegations_from_gouvernorat,
        "localites_from_delegation": localites_from_delegation,
        "all_gouvernorats": all_gouvernorats
    })

@never_cache
@login_required
# Utility functions
def get_delegations_by_gouvernorat(df, nomGouvernorat):
    return df[df['nomGouvernorat'] == nomGouvernorat]['nomDelegation'].unique().tolist()
@never_cache
@login_required
def get_secteurs_by_delegation(df, nomDelegation):
    return df[df['nomDelegation'] == nomDelegation]['nomLocalite'].unique().tolist()
@never_cache
@login_required
def get_all_gouvernorats(df):
    return df['nomGouvernorat'].unique().tolist()
@never_cache
@login_required
def load_delegations(request):
    gouvernorat_id = request.GET.get('gouvernorat_id')
    print(f'Gouvernorat ID: {gouvernorat_id}')  # Debug
    delegations = list(Delegation.objects.filter(gouvernorat_id=gouvernorat_id).values('id', 'nomDelegation'))
    print(f'Delegations: {delegations}')  # Debug
    return JsonResponse(delegations, safe=False)

@never_cache
@login_required
def load_localites(request):
    delegation_id = request.GET.get('delegation_id')
    print(f'Delegation ID: {delegation_id}')  # Debug
    localites = list(Localite.objects.filter(delegation_id=delegation_id).values('id', 'nomLocalite'))
    print(f'Localites: {localites}')  # Debug
    return JsonResponse(localites, safe=False)

@never_cache
@login_required
def ajax_load_code_postal(request):
    localite_id = request.GET.get('localite_id')
    print(f'Localite ID: {localite_id}')  # Debug
    code_postal = get_object_or_404(CodePostal, localite_id=localite_id)
    print(f'Code Postal: {code_postal.codePostal}')  # Debug
    return JsonResponse({'code_postal': code_postal.codePostal})

@never_cache
@login_required
def get_coordinates(request):
    localite_id = request.GET.get('localite_id')
    if localite_id:
        try:
            localite = Localite.objects.get(id=localite_id)
            address = f"{localite.nomLocalite}, {localite.delegation.nomDelegation}, {localite.delegation.gouvernorat.nomGouvernorat}, Tunisia"
            encoded_address = quote(address)
            url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json&limit=1"
            response = requests.get(url)
            data = response.json()
            if data:
                coordinates = {'lat': data[0]['lat'], 'lon': data[0]['lon']}
            else:
                coordinates = {'lat': None, 'lon': None}
        except Localite.DoesNotExist:
            coordinates = {'lat': None, 'lon': None}
        except Exception as e:
            print(f"Error fetching coordinates: {e}")  # Debug
            coordinates = {'lat': None, 'lon': None}
    else:
        coordinates = {'lat': None, 'lon': None}
    return JsonResponse(coordinates)

@staff_member_required
@never_cache
@login_required
def dashboard_view(request):
    current_year = date.today().year
    # Vos calculs de statistiques ici
    sexe_stats = list(Contract.objects.values('civilite').annotate(count=Count('civilite')))
    localite_stats = list(Contract.objects.values('localite__nomLocalite').annotate(count=Count('localite')))
    # age_stats = list(Contract.objects.values('age_range').annotate(count=Count('age_range')))
    
     # Calcul des pourcentages pour les localités
    total_localites = sum([stat['count'] for stat in localite_stats])
    for stat in localite_stats:
        stat['percentage'] = (stat['count'] / total_localites) * 10

     # Statistiques par groupe d'âge
    age_brackets = [(0, 18), (19, 30), (31, 45), (46, 60), (61, 100)]
    age_stats = []
    for lower, upper in age_brackets:
        age_count = Contract.objects.annotate(age=(current_year - ExtractYear('date_naissance'))).filter(age__gte=lower, age__lte=upper).count()
        age_stats.append({'age_range': f'{lower}-{upper}', 'count': age_count})

    # Convertir en JSON
    sexe_stats_json = json.dumps(sexe_stats)
    localite_stats_json = json.dumps(localite_stats)
    age_stats_json = json.dumps(age_stats)

    return render(request, 'contract/dashboard.html', {
        'sexe_stats_json': sexe_stats_json,
        'localite_stats_json': localite_stats_json,
        'age_stats_json': age_stats_json
        
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@never_cache
@login_required
def index_view(request):
    return render(request, 'index.html')

def user_is_admin(user):
    return user.is_staff  # Vérifie si l'utilisateur est un administrateur

@user_passes_test(user_is_admin)
def approved_contracts_view(request):
    approved_contracts = Contract.objects.filter(status='approved')
    return render(request, 'contract/approve_contract.html', {'contracts': approved_contracts})

@user_passes_test(user_is_admin)
def approve_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    
    # S'assurer que le champ created_by est rempli
    if contract.created_by is None:
        contract.created_by = request.user
    
    contract.status = 'approved'
    contract.save()

    messages.success(request, f'Le contrat {contract.id} a été approuvé avec succès.')
    return redirect(request.META.get('HTTP_REFERER', 'approve_contract'))

@user_passes_test(user_is_admin)
def reject_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    
    # S'assurer que le champ created_by est rempli
    if contract.created_by is None:
        contract.created_by = request.user
    
    contract.status = 'rejected'
    contract.save()

    messages.warning(request, f'Le contrat {contract.id} a été rejeté.')
    return redirect(request.META.get('HTTP_REFERER', 'list_contract'))

@user_passes_test(user_is_admin)
@login_required
def list_rejected_contracts(request):
    if request.user.is_staff:  # Seuls les administrateurs peuvent voir cette liste
        rejected_contracts = Contract.objects.filter(status='rejected')
    else:
        rejected_contracts = Contract.objects.none()  # Les revendeurs ne peuvent pas voir cette liste
    
    return render(request, 'contract/rejected_contract.html', {'contracts': rejected_contracts})

# approved/rejected statistics
def contracts_statistics(request):
    # Count approved contracts by month
    approved_contracts = Contract.objects.filter(status='approved').extra({'month': "EXTRACT(month FROM updated_at)"}).values('month').annotate(count=Count('id')).order_by('month')

    # Count rejected contracts by month
    rejected_contracts = Contract.objects.filter(status='rejected').extra({'month': "EXTRACT(month FROM updated_at)"}).values('month').annotate(count=Count('id')).order_by('month')

    # Format data for the charts
    approved_data = {
        "labels": [calendar.month_name[item['month']] for item in approved_contracts],
        "counts": [item['count'] for item in approved_contracts]
    }
    
    rejected_data = {
        "labels": [calendar.month_name[item['month']] for item in rejected_contracts],
        "counts": [item['count'] for item in rejected_contracts]
    }

    context = {
        'approved_data_json': json.dumps(approved_data),
        'rejected_data_json': json.dumps(rejected_data),
    }
    
    return render(request, 'contract/statistics.html', context)
