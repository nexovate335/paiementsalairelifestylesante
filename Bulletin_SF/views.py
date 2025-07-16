from django.shortcuts import render, get_object_or_404
from .models import PrestationMensuelle

def fiche_detail(request, id):
    fiche = get_object_or_404(PrestationMensuelle, id=id)
    # On passe la fiche seule dans le contexte, pour ton template tu peux modifier l'accès
    return render(request, 'Bulletin_SF/liste_fiches.html', {'fiches': [fiche]})
