from django.shortcuts import render
from .models import PrestationMensuelle

def liste_fiches_paie(request):
    fiches = PrestationMensuelle.objects.all()
    return render(request, 'Bulletin_Administration/liste_fiches.html', {'fiches': fiches})
