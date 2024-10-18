from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models import Player, Videogame


@login_required(login_url="/")
def ajouter_jeu_bdd(request):
    if request.user.groups.filter(name="guest").exists():
        request.session["error_not_seen"] = True
        request.session[
            "error_message"
        ] += "Vous n'avez pas l'autorisation de créer un jeu.\\n"
    else:
        # Tests sur le jeu à ajouter dans la BDD
        if (
            (int(request.POST.get("online")) > 0)
            and (int(request.POST.get("hot-seat")) > 0)
            and request.POST.get("nom") != "Nom :"
        ):
            for jeu in Videogame.objects.all():
                if jeu.title.lower() == request.POST.get("nom").lower():
                    print(jeu.title() + " déjà présent.")
                    request.session["error_message"] = (
                        "Erreur : " + jeu.title + " existe déjà.\\n"
                    )
                    request.session["error_not_seen"] = True
                    return redirect("jeux:mes_jeux")
            jeu_f2p = False
            if request.POST.get("f2p") == "True":
                jeu_f2p = True
            jeu_coop = False
            if request.POST.get("coop") == "True":
                jeu_coop = True
            jeu_pvp = False
            if request.POST.get("pvp") == "True":
                jeu_pvp = True
            jeu_a_ajouter = Videogame.objects.create(
                nom=str(request.POST.get("nom")).title(),
                coop=jeu_coop,
                pvp=jeu_pvp,
                f2p=jeu_f2p,
                joueurs_max_online=int(request.POST.get("online")),
                joueurs_max_hot_seat=int(request.POST.get("hot-seat")),
            )
            jeu_a_ajouter.save()
            print(jeu_a_ajouter.title + " correctement ajoute dans la BDD !")
            # Si le jeu est gratuit on le rajoute dans la liste des jeux de tout le monde !!
            if jeu_a_ajouter.f2p:
                for joueur in Player.objects.all():
                    joueur.videogames_list.add(jeu_a_ajouter)
        else:
            request.session["error_message"] += "Erreur dans le jeu à ajouter.\\n"
            request.session["error_not_seen"] = True
    return redirect("jeux:mes_jeux")
