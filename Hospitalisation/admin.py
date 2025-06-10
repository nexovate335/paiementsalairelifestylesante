from django.contrib import admin
from .models import PaiementHospitalisation, ActeurHospitalisation

class ActeurHospitalisationInline(admin.TabularInline):
    model = ActeurHospitalisation
    extra = 1

@admin.register(PaiementHospitalisation)
class PaiementHospitalisationAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant_total', 'msn_montant', 'repartition_detaillee', 'created_at')
    inlines = [ActeurHospitalisationInline]
    readonly_fields = ('msn_montant', 'repartition_detaillee', 'created_at')

    def save_model(self, request, obj, form, change):
        # Enregistre d'abord le paiement
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Enregistre les acteurs liés
        super().save_related(request, form, formsets, change)
        # Une fois que tout est enregistré, appelle la répartition
        form.instance.calcul_repartition()
        form.instance.save()

