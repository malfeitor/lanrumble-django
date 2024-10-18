from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Player, Boardgame
from datetime import time


@login_required(login_url="/")
def ajouter_jeu_societe_bdd(request):
    if request.user.groups.filter(name="guest").exists():
        request.session["error_not_seen"] = True
        request.session[
            "error_message"
        ] += "Vous n'avez pas l'autorisation de créer un jeu.\\n"
    else:
        if (
            int(request.POST.get("joueurs_min")) >= 1
            and int(request.POST.get("joueurs_max")) >= 2
            and len(request.POST.get("nom")) >= 4
            and len(request.POST.get("nom")) < 50
            and (
                int(request.POST.get("temps_prevu_h")) >= 0
                and int(request.POST.get("temps_prevu_min")) >= 0
            )
        ):
            for jeu in Boardgame.objects.all():
                if jeu.title.lower() == request.POST.get("nom").lower():
                    print(jeu.title + " existe déjà.")
                    request.session["error_not_seen"] = True
                    request.session["error_message"] = (
                        "Erreur : " + jeu.title + " existe déjà.\\n"
                    )
                    return redirect("jeux:jeux_societe")
            jeu_ajouter = Boardgame.objects.create(
                nom=str(request.POST.get("nom")).title(),
                complexite=int(request.POST.get("complexite")),
                temps_prevu=time(
                    int(request.POST.get("temps_prevu_h")),
                    int(request.POST.get("temps_prevu_min")),
                ),
                joueurs_min=int(request.POST.get("joueurs_min")),
                joueurs_max=int(request.POST.get("joueurs_max")),
            )
            jeu_ajouter.difficulty = (
                jeu_ajouter.difficulty
                if jeu_ajouter.difficulty < 6 and jeu_ajouter.difficulty > 0
                else 1
            )
            for pseudo in request.POST.getlist("possesseurs"):
                jeu_ajouter.owned_by.add(
                    Player.objects.get(utilisateur=User.objects.get(username=pseudo))
                )
            jeu_ajouter.save()
            print(
                jeu_ajouter.title
                + " correctement enregistré avec l'id "
                + str(jeu_ajouter.id)
            )
        else:
            request.session["error_not_seen"] = True
            request.session[
                "error_message"
            ] += "Erreur dans les informations du jeu.\\n"
    return redirect("jeux:jeux_societe")
