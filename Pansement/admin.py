# Pansement/admin.py
from django.contrib import admin
from .models import Pansement

class PansementAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montantTT', 'maison', 'acteur')
    readonly_fields = ('maison', 'acteur')
