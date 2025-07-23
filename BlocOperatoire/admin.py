from django.contrib import admin
from .models import ( 
        Accouchement, Cesarienne, CureHernie, HVV,ActeMedicalOperatoire,
        ActeMedicalSimple,ActeMedicalIntermediaire,PaiementIVA_IVL,
        ActeTechnique, Varicocele
    )
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
import csv
from django.utils.text import slugify


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

class IntervenantFilterBase(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        values = model_admin.model.objects.values_list(self.parameter_name, flat=True).distinct()
        return [(v, v) for v in values if v]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset


class MedecinFilter(IntervenantFilterBase):
    title = "Médecin"
    parameter_name = "medecin"


class SageFemmeFilter(IntervenantFilterBase):
    title = "Sage-femme"
    parameter_name = "sage_femme"


class AideFilter(IntervenantFilterBase):
    title = "Aide"
    parameter_name = "aide"


class PediatreFilter(IntervenantFilterBase):
    title = "Pédiatre"
    parameter_name = "pediatre"


# ------------------------- Filtres pour Césarienne ------------------------- #

class IntervenantCesarienneFilterBase(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        values = model_admin.model.objects.values_list(self.parameter_name, flat=True).distinct()
        return [(v, v) for v in values if v]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset


class ChirurgienFilter(IntervenantCesarienneFilterBase):
    title = "Chirurgien"
    parameter_name = "chirurgien"


class AnesthesisteFilter(IntervenantCesarienneFilterBase):
    title = "Anesthésiste"
    parameter_name = "anesthesiste"


class AideFilter(IntervenantCesarienneFilterBase):
    title = "Aide"
    parameter_name = "aide"


class PanseurFilter(IntervenantCesarienneFilterBase):
    title = "Panseur"
    parameter_name = "panseur"


class InstrumentisteFilter(IntervenantCesarienneFilterBase):
    title = "Instrumentiste"
    parameter_name = "instrumentiste"


class PediatreFilter(IntervenantCesarienneFilterBase):
    title = "Pédiatre"
    parameter_name = "pediatre"


class SageFemmeFilter(IntervenantCesarienneFilterBase):
    title = "Sage-femme"
    parameter_name = "sage_femme"


@admin.register(Accouchement)
class AccouchementAdmin(BaseAdmin):
    list_display = (
        'libelle', 'montantTT', 'mois', 'annee', 'maison',
        'medecin', 'part_medecin',
        'sage_femme', 'part_sage_femme',
        'aide', 'part_aide',
        'pediatre', 'part_pediatre',
    )

    readonly_fields = (
        'maison',
        'part_medecin',
        'part_sage_femme',
        'part_aide',
        'part_pediatre',
    )

    list_filter = [
        'mois',
        'annee',
        MedecinFilter,
        SageFemmeFilter,
        AideFilter,
        PediatreFilter,
    ]

    ordering = ['-annee', '-mois']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                # Champs ORM uniquement
                totals = qs.aggregate(
                    total_montant=Sum('montantTT'),
                )

                # Champs propriétés (calculés)
                total_maison = sum((obj.maison or 0) for obj in qs)
                total_medecin = sum((obj.part_medecin or 0) for obj in qs)
                total_sage_femme = sum((obj.part_sage_femme or 0) for obj in qs)
                total_aide = sum((obj.part_aide or 0) for obj in qs)
                total_pediatre = sum((obj.part_pediatre or 0) for obj in qs)

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Montant Total : {} FCFA<br>"
                        "Maison : {} FCFA<br>"
                        "Médecin : {} FCFA<br>"
                        "Sage-femme : {} FCFA<br>"
                        "Aide : {} FCFA<br>"
                        "Pédiatre : {} FCFA",
                        totals['total_montant'] or 0,
                        total_maison,
                        total_medecin,
                        total_sage_femme,
                        total_aide,
                        total_pediatre,
                    )
                )
        return response



# ---- Admin complet de Césarienne ----

@admin.register(Cesarienne)
class CesarienneAdmin(BaseAdmin):
    list_display = (
        'libelle', 'montantTT', 'mois', 'annee', 'maison',
        'chirurgien', 'part_chirurgien',
        'anesthesiste', 'part_anesthesiste',
        'aide', 'part_aide',
        'panseur', 'part_panseur',
        'instrumentiste', 'part_instrumentiste',
        'pediatre', 'part_pediatre',
        'sage_femme', 'part_sage_femme',
    )

    readonly_fields = (
        'maison',
        'part_chirurgien',
        'part_anesthesiste',
        'part_aide',
        'part_panseur',
        'part_instrumentiste',
        'part_pediatre',
        'part_sage_femme',
    )

    list_filter = [
        'mois', 'annee',
        ChirurgienFilter,
        AnesthesisteFilter,
        AideFilter,
        PanseurFilter,
        InstrumentisteFilter,
        PediatreFilter,
        SageFemmeFilter,
    ]

    # Totaux filtrés
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                # On fait .aggregate() uniquement sur les champs réels de la DB
                totals_db = qs.aggregate(total=Sum('montantTT'))

                # On calcule en Python ce qui dépend des @property
                maison_total = sum(obj.maison for obj in qs)
                part_chirurgien = sum(obj.part_chirurgien for obj in qs)
                part_anesthesiste = sum(obj.part_anesthesiste for obj in qs)
                part_aide = sum(obj.part_aide for obj in qs)
                part_panseur = sum(obj.part_panseur for obj in qs)
                part_instrumentiste = sum(obj.part_instrumentiste for obj in qs)
                part_pediatre = sum(obj.part_pediatre for obj in qs)
                part_sage_femme = sum(obj.part_sage_femme for obj in qs)

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Montant : {} | Maison : {} | Chirurgien : {} | Anesthésiste : {} | Aide : {}<br>"
                        "Panseur : {} | Instrumentiste : {} | Pédiatre : {} | Sage-femme : {}",
                        totals_db['total'] or 0,
                        maison_total,
                        part_chirurgien,
                        part_anesthesiste,
                        part_aide,
                        part_panseur,
                        part_instrumentiste,
                        part_pediatre,
                        part_sage_femme,
                    )
                )
        return response


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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur=self.value())
        return queryset

# Admin Cure Hernie avec calculs de totaux

@admin.register(CureHernie)
class CureHernieAdmin(BaseAdmin):
    list_display = (
        'libelle', 'montantTT', 'mois', 'annee', 'maison',
        'chirurgien', 'part_chirurgien',
        'aide', 'part_aide',
        'panseur', 'part_panseur',
    )
    readonly_fields = (
        'maison',
        'part_chirurgien',
        'part_aide',
        'part_panseur',
    )
    list_filter = [
        MoisFilter,
        AnneeFilter,
        ChirurgienFilter,
        AideFilter,
        PanseurFilter,
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                total_montant = qs.aggregate(total=Sum('montantTT'))['total'] or 0

                total_maison = sum(obj.maison for obj in qs)
                total_chirurgien = sum(obj.part_chirurgien for obj in qs)
                total_aide = sum(obj.part_aide for obj in qs)
                total_panseur = sum(obj.part_panseur for obj in qs)

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Montant Total : {} | Maison : {} | Chirurgien : {} | Aide : {} | Panseur : {}",
                        total_montant,
                        total_maison,
                        total_chirurgien,
                        total_aide,
                        total_panseur,
                    ),
                    level=messages.INFO
                )
        return response


from django.contrib import admin, messages
from django.db.models import Sum
from django.utils.html import format_html
from .models import HVV


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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien_nom=self.value())
        return queryset

class AnesthesisteFilter(admin.SimpleListFilter):
    title = 'Anesthésiste'
    parameter_name = 'anesthesiste_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('anesthesiste_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(anesthesiste_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset

class InstrumentisteFilter(admin.SimpleListFilter):
    title = 'Instrumentiste'
    parameter_name = 'instrumentiste_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('instrumentiste_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(instrumentiste_nom=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur_nom=self.value())
        return queryset


# Admin personnalisé
@admin.register(HVV)
class HVVAdmin(BaseAdmin):
    list_display = (
        'libelle', 'montant_total', 'mois', 'annee', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
    )
    list_filter = [
        'created_at',
        MoisFilter,
        AnneeFilter,
        ChirurgienFilter,
        AnesthesisteFilter,
        AideFilter,
        InstrumentisteFilter,
        PanseurFilter,
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    chirurgien=Sum('chirurgien_montant'),
                    anesthesiste=Sum('anesthesiste_montant'),
                    aide=Sum('aide_montant'),
                    instrumentiste=Sum('instrumentiste_montant'),
                    panseur=Sum('panseur_montant'),
                )

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Chirurgien : <b>{}</b> | Anesthésiste : <b>{}</b><br>"
                        "Aide : <b>{}</b> | Instrumentiste : <b>{}</b> | Panseur : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['chirurgien'] or 0,
                        totals['anesthesiste'] or 0,
                        totals['aide'] or 0,
                        totals['instrumentiste'] or 0,
                        totals['panseur'] or 0,
                    ),
                    level=messages.INFO
                )
        return response

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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien_nom=self.value())
        return queryset

class AnesthesisteFilter(admin.SimpleListFilter):
    title = 'Anesthésiste'
    parameter_name = 'anesthesiste_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('anesthesiste_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(anesthesiste_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset

class InstrumentisteFilter(admin.SimpleListFilter):
    title = 'Instrumentiste'
    parameter_name = 'instrumentiste_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('instrumentiste_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(instrumentiste_nom=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur_nom'

    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur_nom=self.value())
        return queryset


# Admin personnalisé
@admin.register(ActeMedicalOperatoire)
class ActeMedicalOperatoireAdmin(BaseAdmin):
    list_display = (
        'type_acte', 'libelle', 'mois', 'annee', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'anesthesiste_nom', 'anesthesiste_montant',
        'aide_nom', 'aide_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
    )

    list_filter = [
        'type_acte',
        MoisFilter,
        AnneeFilter,
        'created_at',
        ChirurgienFilter,
        AnesthesisteFilter,
        AideFilter,
        InstrumentisteFilter,
        PanseurFilter,
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    chirurgien=Sum('chirurgien_montant'),
                    anesthesiste=Sum('anesthesiste_montant'),
                    aide=Sum('aide_montant'),
                    instrumentiste=Sum('instrumentiste_montant'),
                    panseur=Sum('panseur_montant'),
                )

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Chirurgien : <b>{}</b> | Anesthésiste : <b>{}</b><br>"
                        "Aide : <b>{}</b> | Instrumentiste : <b>{}</b> | Panseur : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['chirurgien'] or 0,
                        totals['anesthesiste'] or 0,
                        totals['aide'] or 0,
                        totals['instrumentiste'] or 0,
                        totals['panseur'] or 0,
                    ),
                    level=messages.INFO
                )
        return response


# Filtres dynamiques personnalisés
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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur_nom=self.value())
        return queryset


# Admin amélioré
@admin.register(ActeMedicalSimple)
class ActeMedicalSimpleAdmin(BaseAdmin):
    list_display = (
        'type_acte', 'mois', 'annee', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'aide_nom', 'aide_montant',
        'panseur_nom', 'panseur_montant',
        'created_at',
        'repartition_detaillee',
    )

    list_filter = [
        'type_acte',
        MoisFilter,
        AnneeFilter,
        'created_at',
        ChirurgienFilter,
        AideFilter,
        PanseurFilter,
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset

                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    chirurgien=Sum('chirurgien_montant'),
                    aide=Sum('aide_montant'),
                    panseur=Sum('panseur_montant'),
                )

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Chirurgien : <b>{}</b> | Aide : <b>{}</b> | Panseur : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['chirurgien'] or 0,
                        totals['aide'] or 0,
                        totals['panseur'] or 0,
                    ),
                    level=messages.INFO
                )
        return response


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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien_nom=self.value())
        return queryset

class InstrumentisteFilter(admin.SimpleListFilter):
    title = 'Instrumentiste'
    parameter_name = 'instrumentiste_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('instrumentiste_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(instrumentiste_nom=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset


# Admin avec totaux
@admin.register(ActeMedicalIntermediaire)
class ActeMedicalIntermediaireAdmin(BaseAdmin):
    list_display = (
        'type_acte', 'mois', 'annee', 'libelle', 'montant_total', 'msn_montant',
        'chirurgien_nom', 'chirurgien_montant',
        'instrumentiste_nom', 'instrumentiste_montant',
        'panseur_nom', 'panseur_montant',
        'aide_nom', 'aide_montant',
        'created_at',
        'repartition_detaillee',
    )

    list_filter = [
        'type_acte',
        'created_at',
        MoisFilter,
        AnneeFilter,
        ChirurgienFilter,
        InstrumentisteFilter,
        PanseurFilter,
        AideFilter,
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset
                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    chirurgien=Sum('chirurgien_montant'),
                    instrumentiste=Sum('instrumentiste_montant'),
                    panseur=Sum('panseur_montant'),
                    aide=Sum('aide_montant'),
                )

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Chirurgien : <b>{}</b> | Instrumentiste : <b>{}</b> | Panseur : <b>{}</b> | Aide : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['chirurgien'] or 0,
                        totals['instrumentiste'] or 0,
                        totals['panseur'] or 0,
                        totals['aide'] or 0,
                    ),
                    level=messages.INFO
                )
        return response


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

class ActeurFilter(admin.SimpleListFilter):
    title = 'Acteur'
    parameter_name = 'acteur_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('acteur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(acteur_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset


# Admin
@admin.register(PaiementIVA_IVL)
class PaiementIVA_IVLAdmin(BaseAdmin):
    list_display = (
        'libelle', 'mois', 'annee', 'montant_total', 'msn_montant',
        'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant',
        'created_at',
    )

    list_filter = (
        'created_at',
        MoisFilter,
        AnneeFilter,
        ActeurFilter,
        AideFilter,
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset
                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    acteur=Sum('acteur_montant'),
                    aide=Sum('aide_montant'),
                )
                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Acteur : <b>{}</b> | Aide : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['acteur'] or 0,
                        totals['aide'] or 0,
                    ),
                    level=messages.INFO
                )
        return response


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

class ActeurFilter(admin.SimpleListFilter):
    title = 'Acteur'
    parameter_name = 'acteur_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('acteur_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(acteur_nom=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide_nom'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide_nom', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide_nom=self.value())
        return queryset


# Admin
@admin.register(ActeTechnique)
class ActeTechniqueAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'mois', 'annee', 'type',
        'montant_total', 'msn_montant',
        'acteur_nom', 'acteur_montant',
        'aide_nom', 'aide_montant',
        'created_at',
    )
    list_filter = (
        'type',
        'created_at',
        MoisFilter,
        AnneeFilter,
        ActeurFilter,
        AideFilter,
    )
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.calcul_repartition()
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset
                totals = qs.aggregate(
                    total=Sum('montant_total'),
                    msn=Sum('msn_montant'),
                    acteur=Sum('acteur_montant'),
                    aide=Sum('aide_montant'),
                )
                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Total : <b>{}</b> | MSN : <b>{}</b><br>"
                        "Acteur : <b>{}</b> | Aide : <b>{}</b>",
                        totals['total'] or 0,
                        totals['msn'] or 0,
                        totals['acteur'] or 0,
                        totals['aide'] or 0,
                    ),
                    level=messages.INFO
                )
        return response


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

class ChirurgienFilter(admin.SimpleListFilter):
    title = 'Chirurgien'
    parameter_name = 'chirurgien'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('chirurgien', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chirurgien=self.value())
        return queryset

class AideFilter(admin.SimpleListFilter):
    title = 'Aide'
    parameter_name = 'aide'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('aide', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aide=self.value())
        return queryset

class PanseurFilter(admin.SimpleListFilter):
    title = 'Panseur'
    parameter_name = 'panseur'
    def lookups(self, request, model_admin):
        noms = model_admin.model.objects.values_list('panseur', flat=True).distinct()
        return [(n, n) for n in noms if n]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panseur=self.value())
        return queryset


# Admin
@admin.register(Varicocele)
class VaricoceleAdmin(BaseAdmin):
    list_display = (
        'libelle', 'mois', 'annee', 'montantTT', 'maison',
        'chirurgien', 'chirurgien_part',
        'aide', 'aide_part',
        'panseur', 'panseur_part',
    )
    readonly_fields = (
        'maison',
        'chirurgien_part',
        'aide_part',
        'panseur_part',
    )
    list_filter = (
        MoisFilter,
        AnneeFilter,
        ChirurgienFilter,
        AideFilter,
        PanseurFilter,
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                qs = cl.queryset
                totals = qs.aggregate(
                    total=Sum('montantTT'),
                )
                maison_total = sum([obj.maison for obj in qs])
                chirurgien_total = sum([obj.chirurgien_part for obj in qs])
                aide_total = sum([obj.aide_part for obj in qs])
                panseur_total = sum([obj.panseur_part for obj in qs])

                self.message_user(
                    request,
                    format_html(
                        "<b>Totaux filtrés :</b><br>"
                        "Montant total : <b>{}</b> | Maison : <b>{}</b><br>"
                        "Chirurgien : <b>{}</b> | Aide : <b>{}</b> | Panseur : <b>{}</b>",
                        totals['total'] or 0,
                        maison_total or 0,
                        chirurgien_total or 0,
                        aide_total or 0,
                        panseur_total or 0,
                    ),
                    level=messages.INFO
                )
        return response
