from django.shortcuts import get_object_or_404, render
from .models import FicheDePaie

def fiche_detail(request, id):
    fiche = get_object_or_404(FicheDePaie, pk=id)
    return render(request, 'Bulletin_Administration/liste_fiches.html', {'fiches': [fiche]})
