from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Player, VideogameRating
from .gestionnaire_erreur import gestionnaire_erreur
from .joueur_options import joueur_colors, joueur_background


@login_required(login_url="/")
@gestionnaire_erreur
def accueil(request, error_message=False):
    try:
        joueur = Player.objects.get(utilisateur=request.user.id)
    except Exception:
        request.session["error_message"] += "Utilisateur introuvable.\\n"
        request.session["error_not_seen"] = False
        return redirect("jeux:index")
    else:
        amis = {}
        liste_jeux = {}
        for ami in joueur.friends.exclude(utilisateur__groups__name="guest").all():
            amis[ami.utilisateur.username] = []
            for jeu in ami.liste_jeux.all():
                try:
                    vote = (
                        VideogameRating.objects.filter(joueur_concerne=ami.id)
                        .filter(jeu_concerne=jeu.id)
                        .get()
                        .rating
                    )
                except Exception:
                    vote = 5
                amis[ami.utilisateur.username].append([jeu.nom, vote])

        for jeu in joueur.videogames_list.all():
            liste_jeux[jeu.nom] = {}
            liste_jeux[jeu.nom]["id"] = jeu.id
            liste_jeux[jeu.nom]["pvp"] = jeu.pvp
            liste_jeux[jeu.nom]["coop"] = jeu.coop
            liste_jeux[jeu.nom]["f2p"] = jeu.f2p
            liste_jeux[jeu.nom]["joueurs_online"] = jeu.joueurs_max_online
            liste_jeux[jeu.nom]["joueurs_hot_seat"] = jeu.joueurs_max_hot_seat
            try:
                liste_jeux[jeu.nom]["my_vote"] = (
                    VideogameRating.objects.filter(joueur_concerne=joueur.id)
                    .filter(jeu_concerne=jeu.id)
                    .get()
                    .rating
                )
            except Exception:
                liste_jeux[jeu.nom]["my_vote"] = 5

        if User.objects.get(username=joueur.utilisateur).email == "":
            request.session[
                "error_message"
            ] += "Veuillez remplir votre addresse mail dans Mon Compte.\\n"
            request.session["error_not_seen"] = False

        return render(
            request,
            "jeux/accueil.html",
            {
                "amis": amis,
                "liste_jeux": liste_jeux,
                "colors": joueur_colors(request.user.id),
                "background_image": joueur_background(request),
            },
        )
