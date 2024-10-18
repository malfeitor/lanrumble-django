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
        joueur = Player.objects.get(user=request.user.id)
    except Exception:
        request.session["error_message"] += "Utilisateur introuvable.\\n"
        request.session["error_not_seen"] = False
        return redirect("jeux:index")
    else:
        amis = {}
        liste_jeux = {}
        for ami in joueur.friends.exclude(user__groups__name="guest").all():
            amis[ami.user.username] = []
            for jeu in ami.videogames_list.all():
                try:
                    vote = (
                        VideogameRating.objects.filter(joueur_concerne=ami.id)
                        .filter(jeu_concerne=jeu.id)
                        .get()
                        .rating
                    )
                except Exception:
                    vote = 5
                amis[ami.user.username].append([jeu.title, vote])

        for jeu in joueur.videogames_list.all():
            liste_jeux[jeu.title] = {}
            liste_jeux[jeu.title]["id"] = jeu.id
            liste_jeux[jeu.title]["pvp"] = jeu.pvp
            liste_jeux[jeu.title]["coop"] = jeu.coop
            liste_jeux[jeu.title]["f2p"] = jeu.f2p
            liste_jeux[jeu.title]["joueurs_online"] = jeu.max_online_players
            liste_jeux[jeu.title]["joueurs_hot_seat"] = jeu.max_hot_seat_players
            try:
                liste_jeux[jeu.title]["my_vote"] = (
                    VideogameRating.objects.filter(player=joueur.id)
                    .filter(videogame=jeu.id)
                    .get()
                    .rating
                )
            except Exception:
                liste_jeux[jeu.title]["my_vote"] = 5

        if User.objects.get(username=joueur.user).email == "":
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
