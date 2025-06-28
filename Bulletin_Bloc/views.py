from django.shortcuts import render
from .models import FicheDePaie

def liste_fiches_paie(request):
    fiches = FicheDePaie.objects.all()
    return render(request, 'Bulletin_Administration/liste_fiches.html', {'fiches': fiches})
