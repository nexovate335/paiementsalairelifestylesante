from django.contrib.admin import AdminSite
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

class MyAdminSite(AdminSite):
    site_header = "Administration Lifestyle Santé"
    site_title = "Panneau de Contrôle"
    index_title = "Bienvenue dans l'espace d'administration de Paiement salaire"

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = ['css/admin_custom.css']
        return context

admin_site = MyAdminSite(name='myadmin')

# === IMPORTS ADMIN ET MODELS ===

# Acte ORL
from ActeORL.admin import ActeORLAdmin
from ActeORL.models import ActeORL

# Fiches de paie
from Bulletin_Adminstration.admin import FicheDePaieAdmin as FicheDePaieAdmin1
from Bulletin_Adminstration.models import FicheDePaie as FicheDePaie1
from Bulletin_Blanchisserie.admin import FicheDePaieAdmin as FicheDePaieAdmin10
from Bulletin_Blanchisserie.models import FicheDePaie as FicheDePaie10
from Bulletin_Bloc.admin import FicheDePaieAdmin as FicheDePaieAdmin2
from Bulletin_Bloc.models import FicheDePaie as FicheDePaie2
from Bulletin_Caissiere.admin import FicheDePaieAdmin as FicheDePaieAdmin3
from Bulletin_Caissiere.models import FicheDePaie as FicheDePaie3
from Bulletin_GestionPharmacie.admin import FicheDePaieAdmin as FicheDePaieAdmin4
from Bulletin_GestionPharmacie.models import FicheDePaie as FicheDePaie4
from Bulletin_laboratoire.admin import FicheDePaieAdmin as FicheDePaieAdmin5
from Bulletin_laboratoire.models import FicheDePaie as FicheDePaie5
from Bulletin_MedecinConsultant.admin import FicheDePaieAdmin as FicheDePaieAdmin6
from Bulletin_MedecinConsultant.models import FicheDePaie as FicheDePaie6
from Bulletin_Menage.admin import FicheDePaieAdmin as FicheDePaieAdmin7
from Bulletin_Menage.models import FicheDePaie as FicheDePaie7
from Bulletin_Pharmacie.admin import FicheDePaieAdmin as FicheDePaieAdmin8
from Bulletin_Pharmacie.models import FicheDePaie as FicheDePaie8
from Bulletin_Securite.admin import FicheDePaieAdmin as FicheDePaieAdmin9
from Bulletin_Securite.models import FicheDePaie as FicheDePaie9

# Médecins, paramédicaux, SF
from Bulletin_Medecin.admin import FichePrestationAdmin
from Bulletin_Medecin.models import FichePrestation
from Bulletin_paramedicaux.admin import PrestationMensuelleAdmin
from Bulletin_paramedicaux.models import PrestationMensuelle
from Bulletin_SF.admin import PrestationMensuelleAdmin as PMAdmin
from Bulletin_SF.models import PrestationMensuelle as PM

# Bloc opératoire
from BlocOperatoire.admin import (
    AccouchementAdmin, CesarienneAdmin, CureHernieAdmin, HVVAdmin,
    ActeMedicalAdmin, ActeMedicalSimpleAdmin, ActeMedicalIntermediaireAdmin,
    PaiementIVA_IVLAdmin, ActeTechniqueAdmin,VaricoceleAdmin
)
from BlocOperatoire.models import (
    Accouchement, Cesarienne, CureHernie, HVV,
    ActeMedical, ActeMedicalSimple, ActeMedicalIntermediaire,
    PaiementIVA_IVL, ActeTechnique,Varicocele
)

# Laboratoire
from Laboratoire.admin import LaboTriosAdmin, LaboratoireMaisonAdmin
from Laboratoire.models import LaboTrios, LaboratoireMaison

# Charges obligatoires
from ChargeObligatoire.admin import ChargeObligatoireAdmin, MontantTotalAdmin
from ChargeObligatoire.models import ChargeObligatoire, MontantTotal

# Consultations
from Consultation.admin import ConsultationAdmin, CertificatMedicalAdmin
from Consultation.models import Consultation, CertificatMedical

# Échographie
from Echographie.admin import ActeMedicalAdmin as ActeMedicalSimpleAdmin, PaiementMonitorageAdmin
from Echographie.models import ActeMedical as ActeMedicalSimple, PaiementMonitorage

# Hospitalisation
from Hospitalisation.admin import PaiementHospitalisationAdmin
from Hospitalisation.models import PaiementHospitalisation

# Pansement
from Pansement.admin import PansementAdmin
from Pansement.models import Pansement

# Pharmacie
from Pharmacie.admin import PharmacieAdmin
from Pharmacie.models import Pharmacie

# Salaires
from Salaires.admin import (
    DocteurSalaireAdmin, PreleveurSalaireAdmin, PratiqueurSalaireAdmin,
    ParaMedicoSalaireAdmin, PrimeTransportAdmin
)
from Salaires.models import (
    DocteurSalaire, PreleveurSalaire, PratiqueurSalaire,
    ParaMedicoSalaire, PrimeTransport
)

# Séparation pourcentage
from SeparationPourcentage.admin import SeparationPourcentageAdmin
from SeparationPourcentage.models import SeparationPourcentage


#Vaccin
from Vaccin.admin import VaccinAdmin
from Vaccin.models import Vaccin

# === ENREGISTREMENTS ===

for model, admin_class in [
    # Fiches de paie
    (FicheDePaie1, FicheDePaieAdmin1),
    (FicheDePaie2, FicheDePaieAdmin2),
    (FicheDePaie3, FicheDePaieAdmin3),
    (FicheDePaie4, FicheDePaieAdmin4),
    (FicheDePaie5, FicheDePaieAdmin5),
    (FicheDePaie6, FicheDePaieAdmin6),
    (FicheDePaie7, FicheDePaieAdmin7),
    (FicheDePaie8, FicheDePaieAdmin8),
    (FicheDePaie9, FicheDePaieAdmin9),
    (FicheDePaie10, FicheDePaieAdmin10),

    # Autres bulletins
    (FichePrestation, FichePrestationAdmin),
    (PrestationMensuelle, PrestationMensuelleAdmin),
    (PM, PMAdmin),

    # Bloc opératoire
    (Accouchement, AccouchementAdmin),
    (Cesarienne, CesarienneAdmin),
    (CureHernie, CureHernieAdmin),
    (HVV, HVVAdmin),
    (ActeMedical, ActeMedicalAdmin),
    (ActeMedicalSimple, ActeMedicalSimpleAdmin),
    (ActeMedicalIntermediaire, ActeMedicalIntermediaireAdmin),
    (PaiementIVA_IVL, PaiementIVA_IVLAdmin),
    (ActeTechnique, ActeTechniqueAdmin),
    (Varicocele,VaricoceleAdmin),

    # Laboratoire
    (LaboTrios, LaboTriosAdmin),
    (LaboratoireMaison, LaboratoireMaisonAdmin),

    # Acte ORL
    (ActeORL, ActeORLAdmin),

    # Charges
    (ChargeObligatoire, ChargeObligatoireAdmin),
    (MontantTotal, MontantTotalAdmin),

    # Consultations
    (Consultation, ConsultationAdmin),
    (CertificatMedical, CertificatMedicalAdmin),

    # Échographie
    (PaiementMonitorage, PaiementMonitorageAdmin),

    # Hospitalisation
    (PaiementHospitalisation, PaiementHospitalisationAdmin),

    # Pansement, pharmacie
    (Pansement, PansementAdmin),
    (Pharmacie, PharmacieAdmin),

    # Salaires
    (DocteurSalaire, DocteurSalaireAdmin),
    (PreleveurSalaire, PreleveurSalaireAdmin),
    (PratiqueurSalaire, PratiqueurSalaireAdmin),
    (ParaMedicoSalaire, ParaMedicoSalaireAdmin),
    (PrimeTransport, PrimeTransportAdmin),

    # Répartition pourcentage
    (SeparationPourcentage, SeparationPourcentageAdmin),

    #Vaccin
    (Vaccin, VaccinAdmin),

    #Varicocele
    (Varicocele, VaricoceleAdmin),
]:
    try:
        admin_site.register(model, admin_class)
    except AlreadyRegistered:
        pass

# Enregistrement automatique des modèles restants
all_models = apps.get_models()
for model in all_models:
    try:
        admin_site.register(model)
    except AlreadyRegistered:
        pass
