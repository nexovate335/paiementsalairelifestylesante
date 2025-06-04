from django.contrib import admin
from .models import Varicocele

@admin.register(Varicocele)
class VaricoceleAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'montantTT', 'maison',
        'chirurgien', 'chirurgien_part',
        'aide', 'aide_part',
        'panseur', 'panseur_part',
    )
    readonly_fields = ('maison', 'chirurgien_part', 'aide_part', 'panseur_part')
