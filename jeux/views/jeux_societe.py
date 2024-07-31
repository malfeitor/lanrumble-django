from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Joueur, Jeu_Societe
from .gestionnaire_erreur import gestionnaire_erreur
from .joueur_options import joueur_colors, joueur_background


@login_required(login_url='/')
@gestionnaire_erreur
def jeux_societe(request):
    liste_jeux = {}
    liste_amis = Joueur.objects.get(utilisateur=request.user.id).amis.exclude(utilisateur__groups__name="guest").all()
    liste_possesseurs_amis = []
    for jeu in Jeu_Societe.objects.all():
        liste_jeux[jeu.id] = {}
        liste_jeux[jeu.id]['possede_par'] = []
        liste_jeux[jeu.id]['nom'] = jeu.nom
        liste_jeux[jeu.id]['temps_prevu'] = jeu.temps_prevu.strftime(
            "%Hh %Mm")
        liste_jeux[jeu.id]['joueurs_max'] = jeu.joueurs_max
        liste_jeux[jeu.id]['joueurs_min'] = jeu.joueurs_min
        liste_jeux[jeu.id]['complexite'] = jeu.complexite
        for possesseur in jeu.possede_par.all():
            if possesseur in liste_amis or possesseur.utilisateur.username == request.user.username:
                liste_jeux[jeu.id]['possede_par'].append(
                    possesseur.utilisateur.username)
                if possesseur.utilisateur.username not in liste_possesseurs_amis:
                    liste_possesseurs_amis.append(
                        possesseur.utilisateur.username)
        if len(liste_jeux[jeu.id]['possede_par']) == 0:
            liste_jeux.pop(jeu.id, None)
    return render(request, 'jeux/jeux_societe.html',
                  {'jeux': liste_jeux, 'possesseurs_amis': liste_possesseurs_amis,
                   'colors': joueur_colors(request.user.id), 'amis': liste_amis, 'background_image': joueur_background(request)})
