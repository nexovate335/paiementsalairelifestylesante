from django.shortcuts import render, get_object_or_404
from .models import FicheDePaie

def fiche_detail(request, id):
    fiche = get_object_or_404(FicheDePaie, id=id)
    # On passe la fiche seule dans le contexte, pour ton template tu peux modifier l'accès
    return render(request, 'Bulletin_securite/liste_fiches.html', {'fiches': [fiche]})
