from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models import Joueur, Jeu


@login_required(login_url='/')
def ajouter_jeu_bdd(request):
    # Tests sur le jeu à ajouter dans la BDD
    if ((int(request.POST.get('online')) > 0) and (int(request.POST.get('hot-seat')) > 0) and
            request.POST.get('nom') != "Nom :"):
        for jeu in Jeu.objects.all():
            if(jeu.nom.lower() == request.POST.get('nom').lower()):
                print(jeu.nom() + " déjà présent.")
                request.session['error_message'] = "Erreur : " + \
                    jeu.nom + " existe déjà.\\n"
                request.session['error_not_seen'] = True
                return redirect('jeux:mes_jeux')
        jeu_f2p = False
        if request.POST.get('f2p') == "True":
            jeu_f2p = True
        jeu_coop = False
        if request.POST.get('coop') == "True":
            jeu_coop = True
        jeu_pvp = False
        if request.POST.get('pvp') == "True":
            jeu_pvp = True
        jeu_a_ajouter = Jeu.objects.create(
            nom=str(request.POST.get('nom')).title(),
            coop=jeu_coop,
            pvp=jeu_pvp,
            f2p=jeu_f2p,
            joueurs_max_online=int(request.POST.get('online')),
            joueurs_max_hot_seat=int(request.POST.get('hot-seat')))
        jeu_a_ajouter.save()
        print(jeu_a_ajouter.nom + " correctement ajoute dans la BDD !")
        # Si le jeu est gratuit on le rajoute dans la liste des jeux de tout le monde !!
        if jeu_a_ajouter.f2p:
            for joueur in Joueur.objects.all():
                joueur.liste_jeux.add(jeu_a_ajouter)
        # TODO: ajouter les votes 5 etoiles a celui qui poste et aux autres si F2P
    else:
        request.session['error_message'] += "Erreur dans le jeu à ajouter.\\n"
        request.session['error_not_seen'] = True
    return redirect('jeux:mes_jeux')
