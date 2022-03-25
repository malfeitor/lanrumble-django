from django.shortcuts import render, redirect
from ..models import Jeu
from .accueil import *
from .ajouter_jeu_societe_bdd import *
from .ajouter_jeu_video_bdd import *
from .gestionnaire_erreur import gestionnaire_erreur
from .info_compte import *
from .jeux_societe import *
from .joueur_options import *
from .login_and_out import *
from .mes_amis import *
from .mes_jeux_video import *


@gestionnaire_erreur
def index(request):
    if request.user.is_authenticated:
        return redirect('jeux:accueil')
    else:
        return render(request, 'jeux/index.html',
                      {'jeux': Jeu.objects.all()})


def bad_request(request, exception):
    request.session['error_message'] = "Erreur 400.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def permission_denied(request, exception):
    request.session['error_message'] = "Erreur 403.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def page_not_found(request, exception):
    request.session['error_message'] = "Erreur 404.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def server_error(request):
    request.session['error_message'] = "Erreur 500.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:logoutside')
