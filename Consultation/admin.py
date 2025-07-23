from django.contrib import admin
from .models import Consultation, CertificatMedical 
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html


import csv
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.text import slugify
from io import BytesIO
from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Admin de base réutilisable pour exporter en Excel, PDF et CSV.
    Surcharger `get_export_fields`, `get_export_headers`, etc.
    """

    actions = ['export_as_excel', 'export_as_pdf', 'export_as_csv']

    def get_export_fields(self, request):
        """Doit retourner une liste des attributs à exporter"""
        return []

    def get_export_headers(self, request):
        """Doit retourner une liste d'en-têtes (même ordre que les fields)"""
        return []

    def get_export_filename_prefix(self, request):
        """Nom de base pour les fichiers exportés"""
        return self.model._meta.model_name

    def get_export_pdf_title(self, request):
        """Titre du PDF"""
        return self.model._meta.verbose_name_plural.capitalize()

    def export_as_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Export"

        fields = self.get_export_fields(request)
        headers = self.get_export_headers(request) or fields

        ws.append(headers)

        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            ws.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"{slugify(self.get_export_filename_prefix(request))}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

    export_as_excel.short_description = "📥 Exporter en Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        fields = self.get_export_fields(request)
        title = self.get_export_pdf_title(request)
        y = height - 50

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, title)
        y -= 30
        p.setFont("Helvetica", 10)

        for obj in queryset:
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 10)
            row = [str(getattr(obj, f)) for f in fields]
            p.drawString(50, y, " | ".join(row))
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        filename = f"{slugify(self.get_export_filename_prefix(request))}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    export_as_pdf.short_description = "📄 Exporter en PDF"

    def export_as_csv(self, request, queryset):
        fields = self.get_export_fields(request)
        headers = self.get_export_headers(request) or fields

        response = HttpResponse(content_type='text/csv')
        filename = f"{slugify(self.get_export_filename_prefix(request))}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(headers)

        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "📄 Exporter en CSV"


class ActeurFilter(admin.SimpleListFilter):
    title = 'Acteur'
    parameter_name = 'acteur_nom'

    def lookups(self, request, model_admin):
        acteurs = model_admin.model.objects.values_list('acteur_nom', flat=True).distinct()
        return [(a, a) for a in acteurs if a]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(acteur_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'

    def lookups(self, request, model_admin):
        aides = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(a, a) for a in aides if a]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset

class MoisFilter(admin.SimpleListFilter):
    title = 'Mois'
    parameter_name = 'mois'

    def lookups(self, request, model_admin):
        mois = model_admin.model.objects.values_list('mois', flat=True).distinct()
        return [(m, m) for m in mois if m]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(mois=self.value())
        return queryset

class AnneeFilter(admin.SimpleListFilter):
    title = 'Année'
    parameter_name = 'annee'

    def lookups(self, request, model_admin):
        annees = model_admin.model.objects.values_list('annee', flat=True).distinct()
        return [(a, a) for a in annees if a]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(annee=self.value())
        return queryset

@admin.register(Consultation)
class ConsultationAdmin(BaseAdmin):
    list_display = (
        'libelle', 'type', 'montant_total', 'mois', 'annee',
        'montant_type_mensuel',  # Champ calculé
        'msn_montant', 'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant', 'created_at',
    )
    list_filter = ('type', 'created_at', ActeurFilter, AideFilter, MoisFilter, AnneeFilter)
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

    def montant_type_mensuel(self, obj):
        total = Consultation.objects.filter(
            type=obj.type,
            mois=obj.mois,
            annee=obj.annee
        ).aggregate(total=Sum('montant_total'))['total'] or 0
        return total
    montant_type_mensuel.short_description = "Total mensuel par type"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            cl = response.context_data['cl']
            qs = cl.queryset
            total_montant = qs.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
            total_acteur = qs.aggregate(Sum('acteur_montant'))['acteur_montant__sum'] or 0
            total_aide = qs.aggregate(Sum('aide_montant'))['aide_montant__sum'] or 0

            # Affichage directement dans la page via un message info
            self.message_user(
                request,
                format_html(
                    "<b>Totaux (filtres appliqués) :</b> Montant total = {} | Acteur = {} | Aide = {}",
                    total_montant, total_acteur, total_aide
                )
            )
        except Exception:
            pass
        return response


# Admin CertificatMedical
@admin.register(CertificatMedical)
class CertificatMedicalAdmin(BaseAdmin):
    list_display = (
        'libelle', 'montant_total', 'mois', 'annee',
        'msn_nom', 'msn_montant',
        'acteur_nom', 'acteur_montant',
        'created_at'
    )
    readonly_fields = ('msn_montant', 'acteur_montant', 'created_at')

    list_filter = (ActeurFilter, MoisFilter, AnneeFilter)
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            cl = response.context_data['cl']
            qs = cl.queryset
            total_montant = qs.aggregate(Sum('montant_total'))['montant_total__sum'] or 0
            total_acteur = qs.aggregate(Sum('acteur_montant'))['acteur_montant__sum'] or 0
            total_msn = qs.aggregate(Sum('msn_montant'))['msn_montant__sum'] or 0

            self.message_user(
                request,
                format_html(
                    "<b>Totaux (filtres appliqués) :</b> Montant total = {} | Acteur = {} | Maison = {}",
                    total_montant, total_acteur, total_msn
                )
            )
        except Exception:
            pass
        return response


