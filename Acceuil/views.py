from django.shortcuts import render

def page_accueil(request):
    return render(request, 'Acceuil/accueil.html')  # attention au chemin
