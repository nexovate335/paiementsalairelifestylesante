from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Acceuil.urls')),
    path('Bulletin_Adminstration/', include('Bulletin_Adminstration.urls')),  # ← inclusion des urls de l'app
    path('Bulletin_Blanchisserie/', include('Bulletin_Blanchisserie.urls')),
    path('Bulletin_Bloc/', include('Bulletin_Bloc.urls')),
    path('Bulletin_Caissiere/', include('Bulletin_Caissiere.urls')),
    path('Bulletin_GestionPharmacie/', include('Bulletin_GestionPharmacie.urls')),
    path('Bulletin_laboratoire/', include('Bulletin_laboratoire.urls')),
    path('Bulletin_Medecin/', include('Bulletin_Medecin.urls')),
    path('Bulletin_MedecinConsultant/', include('Bulletin_MedecinConsultant.urls')),
    path('Bulletin_Menage/', include('Bulletin_Menage.urls')),
    path('Bulletin_paramedicaux/', include('Bulletin_paramedicaux.urls')),
    path('Bulletin_Pharmacie/', include('Bulletin_Pharmacie.urls')),
    path('Bulletin_Securite/', include('Bulletin_Securite.urls')),
    path('Bulletin_SF/', include('Bulletin_SF.urls')),
    # ajoute d'autres apps ici
]
