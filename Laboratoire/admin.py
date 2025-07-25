from django.contrib import admin
from .models import LaboTrios, LaboratoireMaison
from django.db.models import Sum
from django.utils.html import format_html
from django.contrib import admin

# BaseAdmin = admin avec export Excel, PDF, CSV (déjà vu précédemment)
class BaseAdmin(admin.ModelAdmin):
    actions = ['export_as_excel', 'export_as_pdf', 'export_as_csv']

    def get_export_fields(self, request):
        return []

    def get_export_headers(self, request):
        return []

    def get_export_filename_prefix(self, request):
        return self.model._meta.model_name

    def get_export_pdf_title(self, request):
        return self.model._meta.verbose_name_plural.capitalize()

    def export_as_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse
        from django.utils.text import slugify

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Export"

        fields = self.get_export_fields(request)
        headers = self.get_export_headers(request) or fields
        ws.append(headers)

        for obj in queryset:
            ws.append([getattr(obj, field) for field in fields])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{slugify(self.get_export_filename_prefix(request))}.xlsx"'
        wb.save(response)
        return response

    export_as_excel.short_description = "📥 Exporter en Excel"

    def export_as_pdf(self, request, queryset):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from io import BytesIO
        from django.http import HttpResponse
        from django.utils.text import slugify

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, self.get_export_pdf_title(request))
        y -= 30
        p.setFont("Helvetica", 10)

        fields = self.get_export_fields(request)
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
        response['Content-Disposition'] = f'attachment; filename="{slugify(self.get_export_filename_prefix(request))}.pdf"'
        return response

    export_as_pdf.short_description = "📄 Exporter en PDF"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.text import slugify

        fields = self.get_export_fields(request)
        headers = self.get_export_headers(request) or fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{slugify(self.get_export_filename_prefix(request))}.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(headers)

        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "📄 Exporter en CSV"


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

class PreleveurFilter(admin.SimpleListFilter):
    title = 'Préleveur'
    parameter_name = 'preleveur_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('preleveur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(preleveur_nom=self.value())
        return queryset

class PrescripteurFilter(admin.SimpleListFilter):
    title = 'Prescripteur'
    parameter_name = 'prescripteur_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('prescripteur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(prescripteur_nom=self.value())
        return queryset


class TechnicienFilter(admin.SimpleListFilter):
    title = 'Technicien'
    parameter_name = 'technicien_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('technicien_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(technicien_nom=self.value())
        return queryset
        

class AssistanteFilter(admin.SimpleListFilter):
    title = 'Assistante'
    parameter_name = 'assistante_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('assistante_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(assistante_nom=self.value())
        return queryset


@admin.register(LaboTrios)
class LaboTriosAdmin(BaseAdmin):
    list_display = (
        'libelle', 'mois', 'annee', 'tarif_maison', 'tarif_trios', 'benefice_maison',
        'msn_part_tarif_trios', 'total_g', 'msn_final', 'acteurs_total','prescripteur_nom', 'prescripteur_montant',
        'preleveur_nom', 'preleveur_montant' 
    )
    readonly_fields = (
        'benefice_maison', 'msn_part_tarif_trios', 'total_g', 'msn_final',
        'acteurs_total', 'preleveur_montant', 'prescripteur_montant', 'created_at'
    )
    ordering = ('-created_at',)

    list_filter = (MoisFilter, AnneeFilter, PreleveurFilter, PrescripteurFilter)

    # 🌟 Pour l’export
    def get_export_fields(self, request):
        return [
            'libelle', 'mois', 'annee', 'tarif_maison', 'tarif_trios',
            'benefice_maison', 'msn_part_tarif_trios', 'total_g',
            'msn_final', 'acteurs_total', 'preleveur_nom', 'preleveur_montant',
            'prescripteur_nom', 'prescripteur_montant', 'created_at'
        ]

    def get_export_headers(self, request):
        return [
            'Libellé', 'Mois', 'Année', 'Tarif maison', 'Tarif trios',
            'Bénéfice maison', 'Part MSN', 'Total G', 'MSN Final',
            'Total Acteurs', 'Préleveur', 'Montant Préleveur',
            'Prescripteur', 'Montant Prescripteur', 'Date création'
        ]

    def get_export_filename_prefix(self, request):
        return "labo-trios"

    def get_export_pdf_title(self, request):
        return "Rapport Labo Trios"

    def changelist_view(self, request, extra_context=None):
        # même logique que précédemment : totaux filtrés affichés
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            cl = response.context_data['cl']
            qs = cl.queryset

            totals = qs.aggregate(
                tarif_maison_total=Sum('tarif_maison'),
                tarif_trios_total=Sum('tarif_trios'),
                benefice_maison_total=Sum('benefice_maison'),
                msn_final_total=Sum('msn_final'),
                acteurs_total_total=Sum('acteurs_total'),
                preleveur_total=Sum('preleveur_montant'),
                prescripteur_total=Sum('prescripteur_montant'),
            )

            self.message_user(
                request,
                format_html(
                    "<b>Totaux filtrés :</b><br>"
                    "Tarif maison : {} | Tarif trios : {} | Bénéfice maison : {}<br>"
                    "MSN final : {} | Acteurs total : {}<br>"
                    "Préleveur : {} | Prescripteur : {}",
                    totals['tarif_maison_total'] or 0,
                    totals['tarif_trios_total'] or 0,
                    totals['benefice_maison_total'] or 0,
                    totals['msn_final_total'] or 0,
                    totals['acteurs_total_total'] or 0,
                    totals['preleveur_total'] or 0,
                    totals['prescripteur_total'] or 0,
                )
            )
        except Exception:
            pass

        return response


@admin.register(LaboratoireMaison)
class LaboratoireMaisonAdmin(BaseAdmin):
    list_display = (
        'libelle', 'mois', 'annee', 'montant_total', 'msn_part', 'acteurs_part',
        'prescripteur_nom', 'prescripteur_gain',
        'technicien_nom', 'technicien_gain',
        'preleveur_nom', 'preleveur_gain',
        'assistante_nom', 'assistante_gain',
    )
    ordering = ['-annee', '-mois']
    list_filter = [
        MoisFilter, AnneeFilter, PrescripteurFilter,
        TechnicienFilter, PreleveurFilter, AssistanteFilter
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            cl = response.context_data['cl']
            qs = cl.queryset

            totals = qs.aggregate(
                total_montant=Sum('montant_total'),
                total_msn=Sum('msn_part'),
                total_acteurs=Sum('acteurs_part'),
                total_prescripteur=Sum('prescripteur_gain'),
                total_technicien=Sum('technicien_gain'),
                total_preleveur=Sum('preleveur_gain'),
                total_assistante=Sum('assistante_gain'),
            )

            self.message_user(
                request,
                format_html(
                    "<b>Totaux filtrés :</b><br>"
                    "Montant total : {} | MSN : {} | Acteurs : {}<br>"
                    "Prescripteur : {} | Technicien : {} | Préleveur : {} | Assistante : {}",
                    totals['total_montant'] or 0,
                    totals['total_msn'] or 0,
                    totals['total_acteurs'] or 0,
                    totals['total_prescripteur'] or 0,
                    totals['total_technicien'] or 0,
                    totals['total_preleveur'] or 0,
                    totals['total_assistante'] or 0,
                )
            )
        except Exception:
            pass
        return response

    def get_export_fields(self, request):
        return [
            'libelle', 'mois', 'annee', 'montant_total', 'msn_part', 'acteurs_part',
            'prescripteur_nom', 'prescripteur_gain',
            'technicien_nom', 'technicien_gain',
            'preleveur_nom', 'preleveur_gain',
            'assistante_nom', 'assistante_gain'
        ]

    def get_export_headers(self, request):
        return [
            'Libellé', 'Mois', 'Année', 'Montant total', 'Part MSN', 'Part Acteurs',
            'Prescripteur', 'Gain Prescripteur',
            'Technicien', 'Gain Technicien',
            'Préleveur', 'Gain Préleveur',
            'Assistante', 'Gain Assistante'
        ]

    def get_export_filename_prefix(self, request):
        return "laboratoire-maison"

    def get_export_pdf_title(self, request):
        return "Rapport Laboratoire Maison"
