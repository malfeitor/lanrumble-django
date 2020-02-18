from django.shortcuts import render, get_object_or_404, redirect
from django.http import QueryDict, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from datetime import time, datetime
from os import path
from django.conf import settings
from .models import Jeu, Joueur, Jeu_Societe, Vote_Jeu_Video
from .forms import ConfigColorsForm


log_dir = '/var/log/nginx/'
log_file = 'user_connections.log'

def joueur_colors(joueur_id):
    """Fonction pour avoir la liste des couleurs de l'utilisateur logé"""
    try:
        joueur = Joueur.objects.get(utilisateur=joueur_id)
    except Exception as e:
        print(e)
    return {
        'body_background': joueur.color_body_background,
        'body_text': joueur.color_body_text,
        'nav_background': joueur.color_nav_background,
        'nav_link_active': joueur.color_nav_link_active,
        'nav_link_hover': joueur.color_nav_link_hover,
        'nav_link': joueur.color_nav_link,
        'nav_text': joueur.color_nav_text
    }


def joueur_background(request):
    """Fonction pour avoir le fond d'écran de l'utilisateur logé"""
    try:
        background_image = Joueur.objects.get(
            utilisateur=request.user.id).background_file.url
    except Exception as e:
        background_image = ""
    return background_image


def gestionnaire_erreur(func):
    """Fonction qui gère les erreurs"""
    def inner(request, *args, **kwargs):
        if 'error_not_seen' in request.session and 'error_message' in request.session:
            if request.session['error_not_seen']:
                request.session['error_not_seen'] = False
            else:
                request.session['error_message'] = ''
        else:
            request.session['error_message'] = ''
            request.session['error_not_seen'] = False
        return func(request, *args, **kwargs)
    return inner


def is_user_connected(func):
    """Décorateur pour vérifier si l'utilisateur est bien connecté"""
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('jeux:index')
        else:
            return func(request, *args, **kwargs)
    return inner

@gestionnaire_erreur
def index(request):
    if request.user.is_authenticated:
        return redirect('jeux:accueil')
    else:
        return render(request, 'jeux/index.html',
                      {'jeux': Jeu.objects.all()})


def loginside(request):
    """Vue de connection"""
    pseud = request.POST.get('pseudo')
    passwd = request.POST.get('password')
    user = authenticate(request, username=pseud, password=passwd)
    if user is not None:
        login(request, user)
    else:
        with open(path.join(log_dir, log_file), 'a') as log_file_opened:
            log_file_opened.write(request.META['HTTP_X_REAL_IP']+' - '+
                datetime.now().strftime("%Y/%m/%d %H:%M:%S")+' - '+pseud+'\n')
        request.session['error_message'] += 'Login ou mot de passe incorrect.\\n'
        request.session['error_not_seen'] = True
        return redirect('jeux:index')
    try:
        joueur = Joueur.objects.get(utilisateur=user.id)
        joueur.utilisateur.check_password(passwd)
    except Exception as e:
        request.session['error_message'] += 'Utilisateur introuvable.\\n'
        request.session['error_not_seen'] = True
        return render(request, 'jeux/index.html',
                      {'jeux': Jeu.objects.all()})
    else:
        request.session['pseudo'] = joueur.utilisateur.username
        return redirect('jeux:accueil')


def logoutside(request):
    if request.user.is_authenticated:
        request.session.clear()
        logout(request)
    return redirect('jeux:index')

@is_user_connected
@gestionnaire_erreur
def accueil(request, error_message=False):
    try:
        joueur = Joueur.objects.get(utilisateur=request.user.id)
    except Exception as e:
        request.session['error_message'] += 'Utilisateur introuvable.\\n'
        request.session['error_not_seen'] = False
        return redirect('jeux:index')
    else:
        amis = {}
        liste_jeux = {}
        for ami in joueur.amis.all():
            amis[ami.utilisateur.username] = []
            for jeu in ami.liste_jeux.all():
                try:
                    vote = Vote_Jeu_Video.objects.filter(joueur_concerne=ami.id).filter(jeu_concerne=jeu.id).get().valeur
                except Exception as e:
                    vote = 5
                amis[ami.utilisateur.username].append([jeu.nom, vote])

        for jeu in joueur.liste_jeux.all():
            liste_jeux[jeu.nom] = {}
            liste_jeux[jeu.nom]['id'] = jeu.id
            liste_jeux[jeu.nom]['pvp'] = jeu.pvp
            liste_jeux[jeu.nom]['coop'] = jeu.coop
            liste_jeux[jeu.nom]['f2p'] = jeu.f2p
            liste_jeux[jeu.nom]['joueurs_online'] = jeu.joueurs_max_online
            liste_jeux[jeu.nom]['joueurs_hot_seat'] = jeu.joueurs_max_hot_seat
            try:
                liste_jeux[jeu.nom]['my_vote'] = Vote_Jeu_Video.objects.filter(joueur_concerne=joueur.id).filter(jeu_concerne=jeu.id).get().valeur
            except Exception as e:
                liste_jeux[jeu.nom]['my_vote'] = 5
        # TODO DOING: alerter l'user si il n'a pas mis son mail dans la bdd
        if (User.objects.get(username=joueur.utilisateur).email == ""):
            request.session['error_message'] += 'Veuillez remplir votre addresse mail dans Mon Compte.\\n'
            request.session['error_not_seen'] = False

        return render(request, 'jeux/accueil.html',
                      {'amis': amis, 'liste_jeux': liste_jeux,
                       'colors': joueur_colors(request.user.id), 'background_image': joueur_background(request)})


@is_user_connected
@gestionnaire_erreur
def config(request):
    form_colors = ConfigColorsForm(
        instance=Joueur.objects.get(utilisateur=request.user.id))

    return render(request, 'jeux/config.html',
                  {'colors': joueur_colors(request.user.id), 'form_colors': form_colors, 'background_image': joueur_background(request)})


@is_user_connected
def change_info(request):
    if request.user.check_password(request.POST.get('password')) and request.method == 'POST':
        if request.POST.get('password_new_1') != request.POST.get('password_new_1'):
            request.session['error_message'] = "Les nouveaux mots de passe ne correspondent pas.\\n"
            request.session['error_not_seen'] = True
            return redirect('jeux:config')
        elif not request.POST.get('password_new_1') == "":
            request.user.set_password(request.POST.get('password_new_1'))
            login(request, authenticate(
                request, username=request.user.username, password=request.POST.get('password')))
            request.user.save()
            print("Mot de passe changé pour " + request.user.username)
        form = ConfigColorsForm(request.POST, request.FILES, instance=Joueur.objects.get(
            utilisateur=request.user.id))
        if form.is_valid():
            form.clean()
            # On supprimme le fond decran si upload d'un nouveau ou demande de le supprimmer !!
            try:
                if (form.cleaned_data['background_file'] == False
                        or not ('user_' + str(request.user.id) + '/') in str(form.cleaned_data['background_file'])):
                    os.remove(os.path.join(settings.MEDIA_ROOT, Joueur.objects.get(
                        utilisateur=request.user.id).background_file.name))
            except Exception as e:
                print("Error : " + str(e))
            form.save()
        return redirect('jeux:config')
    else:
        request.session['error_message'] += "Mot de passe actuel incorrect.\\n"
        request.session['error_not_seen'] = True
        return redirect('jeux:config')


@is_user_connected
@gestionnaire_erreur
def mes_amis(request):

    return render(request, 'jeux/mes_amis.html',
                  {'colors': joueur_colors(request.user.id), 'background_image': joueur_background(request)})


@is_user_connected
@gestionnaire_erreur
def jeux_societe(request):
    liste_jeux = {}
    liste_amis = Joueur.objects.get(utilisateur=request.user.id).amis.all()
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
                if not possesseur.utilisateur.username in liste_possesseurs_amis:
                    liste_possesseurs_amis.append(
                        possesseur.utilisateur.username)
        if len(liste_jeux[jeu.id]['possede_par']) == 0:
            liste_jeux.pop(jeu.id, None)
    return render(request, 'jeux/jeux_societe.html',
                  {'jeux': liste_jeux, 'possesseurs_amis': liste_possesseurs_amis,
                   'colors': joueur_colors(request.user.id), 'amis': liste_amis, 'background_image': joueur_background(request)})


@is_user_connected
def ajouter_jeu_societe_bdd(request):
    if (int(request.POST.get('joueurs_min')) >= 1 and int(request.POST.get('joueurs_max')) >= 2
        and len(request.POST.get('nom')) > 4 and len(request.POST.get('nom')) < 50
            and (int(request.POST.get('temps_prevu_h')) >= 0 and int(request.POST.get('temps_prevu_min')) >= 0)):
        for jeu in Jeu_Societe.objects.all():
            if(jeu.nom.lower() == request.POST.get('nom').lower()):
                print(jeu.nom + " existe déjà.")
                request.session['error_not_seen'] = True
                request.session['error_message'] = "Erreur : " + \
                    jeu.nom + " existe déjà.\\n"
                return redirect('jeux:jeux_societe')
        jeu_ajouter = Jeu_Societe.objects.create(
            nom=str(request.POST.get('nom')).title(),
            complexite=int(request.POST.get('complexite')),
            temps_prevu=time(int(request.POST.get('temps_prevu_h')), int(
                request.POST.get('temps_prevu_min'))),
            joueurs_min=int(request.POST.get('joueurs_min')),
            joueurs_max=int(request.POST.get('joueurs_max')))
        jeu_ajouter.complexite = jeu_ajouter.complexite if jeu_ajouter.complexite < 6 and jeu_ajouter.complexite > 0 else 1
        for pseudo in request.POST.getlist('possesseurs'):
            jeu_ajouter.possede_par.add(Joueur.objects.get(
                utilisateur=User.objects.get(username=pseudo)))
        jeu_ajouter.save()
        print(jeu_ajouter.nom +
              " correctement enregistré avec l'id " + str(jeu_ajouter.id))
    else:
        request.session['error_not_seen'] = True
        request.session['error_message'] += "Erreur dans les informations du jeu.\\n"
    return redirect('jeux:jeux_societe')


@is_user_connected
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


@is_user_connected
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


@is_user_connected
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


@is_user_connected
def ajouter_jeu_bdd(request):
    # Tests sur le jeu à ajouter dans la BDD
    if ((int(request.POST.get('online')) > 0) and (int(request.POST.get('hot-seat')) > 0)
            and request.POST.get('nom') != "Nom :"):
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


@is_user_connected
def ajax_vote_videogame(request):
    vote_exists = False
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


def bad_request(request):
    request.session['error_message'] = "Erreur 400.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def permission_denied(request):
    request.session['error_message'] = "Erreur 403.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def page_not_found(request):
    request.session['error_message'] = "Erreur 404.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:index')


def server_error(request):
    request.session['error_message'] = "Erreur 500.\\n"
    request.session['error_not_seen'] = True
    return redirect('jeux:logoutside')
