from django.contrib import admin
from .models import Contract  # import your model

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'type_abonnement', 'status')  # Customize this list as per your model fields

# Alternatively, you can register it without the decorator:
# admin.site.register(Contract)
