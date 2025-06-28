from django.shortcuts import render
from .models import FichePrestation

def liste_fiches_paie(request):
    fiches = FichePrestation.objects.all()
    return render(request, 'Bulletin_Administration/liste_fiches.html', {'fiches': fiches})
