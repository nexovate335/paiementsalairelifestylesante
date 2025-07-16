from django.shortcuts import render, get_object_or_404
from .models import FichePrestation

def fiche_detail(request, id):
    fiche = get_object_or_404(FichePrestation, id=id)
    # On passe la fiche seule dans le contexte, pour ton template tu peux modifier l'accès
    return render(request, 'Bulletin_Medecin/liste_fiches.html', {'fiches': [fiche]})
