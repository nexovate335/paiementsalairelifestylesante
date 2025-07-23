from django.contrib import admin
from django.contrib import admin, messages
from django.db.models import Sum
from django.utils.html import format_html
from .models import ActeORL
import csv
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.text import slugify
from io import BytesIO
from reportlab.lib.pagesizes import A4


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



# Filtres personnalisés
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

class LibelleFilter(admin.SimpleListFilter):
    title = 'Libellé'
    parameter_name = 'libelle'

    def lookups(self, request, model_admin):
        libelles = model_admin.model.objects.values_list('libelle', flat=True).distinct()
        return [(l, l) for l in libelles if l]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(libelle=self.value())
        return queryset


# Admin avec totaux filtrés
@admin.register(ActeORL)
class ActeORLAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'mois', 'annee', 'montant_tt', 'montant_msn', 'montant_acteur')
    list_filter = (LibelleFilter, MoisFilter, AnneeFilter)
    readonly_fields = ('montant_msn', 'montant_acteur')

    fieldsets = (
        (None, {
            'fields': ('libelle', 'montant_tt', 'mois', 'annee')
        }),
        ('Montants calculés', {
            'fields': ('montant_msn', 'montant_acteur'),
            'classes': ('collapse',)
        }),
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset
                totals = qs.aggregate(
                    total_tt=Sum('montant_tt'),
                    total_msn=Sum('montant_msn'),
                    total_acteur=Sum('montant_acteur'),
                )

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total TTC : <b>{}</b> | MSN : <b>{}</b> | Acteur : <b>{}</b>",
                        totals['total_tt'] or 0,
                        totals['total_msn'] or 0,
                        totals['total_acteur'] or 0,
                    ),
                    level=messages.INFO
                )
        return response

