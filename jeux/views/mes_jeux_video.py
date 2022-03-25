from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import Joueur, Jeu, Vote_Jeu_Video
from .gestionnaire_erreur import gestionnaire_erreur
from .joueur_options import joueur_colors, joueur_background


@login_required(login_url='/')
@gestionnaire_erreur
def mes_jeux(request):
    jeux_possedes = Joueur.objects.get(
        utilisateur=request.user.id).liste_jeux.all()

    jeux_bdd = list(Jeu.objects.all())
    temp = []
    for jeu in jeux_bdd:
        if not jeu.f2p:
            temp.append(jeu.nom)

    for jeu in jeux_possedes:
        if jeu.nom in temp:
            temp.remove(jeu.nom)

    jeux_bdd = []
    for jeu in temp:
        jeux_bdd.append(Jeu.objects.get(nom=jeu))
    votes = list(Vote_Jeu_Video.objects.filter(joueur_concerne=Joueur.objects.get(utilisateur=request.user.id)))
    return render(request, 'jeux/mes_jeux.html',
                  {'jeux_bdd': jeux_bdd, 'jeux_possedes': jeux_possedes, 'votes': votes,
                   'colors': joueur_colors(request.user.id), 'background_image': joueur_background(request)})


@login_required(login_url='/')
def mes_jeux_ajouter(request):
    joueur = Joueur.objects.get(utilisateur=request.user.id)
    for id_jeu in request.POST.getlist('jeu'):
        joueur_la_pas = True
        for jeu in joueur.liste_jeux.all():
            if str(id_jeu) == str(jeu.id):
                joueur_la_pas = False
        if joueur_la_pas:
            try:
                joueur.liste_jeux.add(Jeu.objects.get(pk=id_jeu))
            except Exception as e:
                print("Erreur ajouter jeu liste de : " +
                      joueur.utilisateur.username + "\\nJeu id = " + id_jeu + "\\n" + e)
                request.session['error_not_seen'] = True
                request.session['error_message'] = "Erreur : " + \
                    jeu.nom + " n'existe pas, ou est déjà dans votre liste.\\n"
    return redirect('jeux:mes_jeux')


@login_required(login_url='/')
def mes_jeux_enlever(request):
    joueur = Joueur.objects.get(utilisateur=request.user.id)
    print(request.POST.getlist('jeu'))
    for id_jeu in request.POST.getlist('jeu'):
        if not get_object_or_404(Jeu, pk=id_jeu).f2p:
            test_it = False
            for jeu in joueur.liste_jeux.all():
                if str(id_jeu) == str(jeu.id):
                    test_it = True
            if test_it:
                try:
                    joueur.liste_jeux.remove(Jeu.objects.get(pk=id_jeu))
                except Exception as e:
                    print("Erreur enlever jeu liste de : " +
                          joueur.utilisateur.username + "\\nJeu id = " + id_jeu + "\\n" + str(e))
                    request.session['error_not_seen'] = False
                    request.session['error_message'] = "Erreur : " + \
                        jeu.nom + " n'existe pas, ou n'est pas dans votre liste.\\n"
    joueur.save()
    return redirect('jeux:mes_jeux')


@login_required(login_url='/')
def ajax_vote_videogame(request):
    # vote_exists = False
    vote_value = request.POST.get('vote')
    game = Jeu.objects.get(id=request.POST.get('jeu')[3:])
    player = Joueur.objects.get(utilisateur=request.user.id)
    vote = Vote_Jeu_Video.objects.filter(jeu_concerne=game).filter(joueur_concerne=player)
    if len(vote) == 0:
        vote = Vote_Jeu_Video(valeur=vote_value, jeu_concerne=game, joueur_concerne=player)
        vote.save()
    else:
        vote[0].valeur = vote_value
        vote[0].save()
    return HttpResponse(200)
