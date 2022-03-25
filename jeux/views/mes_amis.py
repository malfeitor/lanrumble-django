from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .joueur_options import joueur_colors, joueur_background
from .gestionnaire_erreur import gestionnaire_erreur


@login_required(login_url='/')
@gestionnaire_erreur
def mes_amis(request):
    return render(request, 'jeux/mes_amis.html',
                  {'colors': joueur_colors(request.user.id), 'background_image': joueur_background(request)})
