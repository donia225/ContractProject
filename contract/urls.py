from django import views
from django.urls import path
from .views import add_contract, approve_contract, approved_contracts_view, dashboard_view, details_contract, edit_contract, list_contract, get_all_gouvernorats, list_rejected_contracts, load_delegations, load_localites, ajax_load_code_postal, logout_view, reject_contract, test_view, get_coordinates



urlpatterns = [
    path('add/', add_contract, name='add_contract'),
    path('list/', list_contract, name='list_contract'),
    path('edit/<int:contract_id>/', edit_contract, name='edit_contract'),
    path('details/<int:contract_id>/', details_contract, name='details_contract'),
    path('ajax/load-gouvernorats/', get_all_gouvernorats, name='ajax_load_gouvernorats'),
    path('ajax/load-delegations/', load_delegations, name='ajax_load_delegations'),
    path('ajax/load-localites/', load_localites, name='ajax_load_localites'),
    path('ajax/load-code-postal/', ajax_load_code_postal, name='ajax_load_code_postal'),
    path('test-view/', test_view, name='test_view'),
    path('get_coordinates/', get_coordinates, name='get_coordinates'),
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('logout/', logout_view, name='logout'),
    path('approve/<int:contract_id>/', approve_contract, name='approve_contract'),
    path('reject/<int:contract_id>/', reject_contract, name='reject_contract'),
    path('approved-contracts/', approved_contracts_view, name='approved_contracts'),
    path('rejected/', list_rejected_contracts, name='list_rejected_contracts'),
    

    
]
