from .models import Pharmacie  # assume que ton modèle est déjà importé
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
import openpyxl
from io import BytesIO
from django.contrib import admin
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.text import slugify
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


@admin.register(Pharmacie)
class PharmacieAdmin(BaseAdmin):
    list_display = (
        'libelle', 
        'prix_vente',
        'mois',
        'annee', 
        'benefice', 
        'maison', 
        'controleur', 
        'vendeur', 
        'prescripteur',
    )

    readonly_fields = (
        'benefice',
        'maison',
        'controleur',
        'vendeur',
        'prescripteur',
    )

    list_filter = [MoisFilter, AnneeFilter]
    ordering = ['-annee', '-mois']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                # Champs ORM uniquement
                totals = qs.aggregate(
                    total_prix_vente=Sum('prix_vente'),
                )

                # Propriétés calculées (non ORM)
                total_benefice = sum((obj.benefice or 0) for obj in qs)
                total_maison = sum((obj.maison or 0) for obj in qs)
                total_controleur = sum((obj.controleur or 0) for obj in qs)
                total_vendeur = sum((obj.vendeur or 0) for obj in qs)
                total_prescripteur = sum((obj.prescripteur or 0) for obj in qs)

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Prix de vente total : {} FCFA<br>"
                        "Bénéfice total : {} FCFA<br>"
                        "Maison : {} FCFA<br>"
                        "Contrôleur : {} FCFA<br>"
                        "Vendeur : {} FCFA<br>"
                        "Prescripteur : {} FCFA",
                        totals['total_prix_vente'] or 0,
                        total_benefice,
                        total_maison,
                        total_controleur,
                        total_vendeur,
                        total_prescripteur,
                    )
                )
        return response
