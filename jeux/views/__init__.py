from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse    # QueryDict,
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, password_validation
# from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ..models import Jeu, Joueur, Jeu_Societe, Vote_Jeu_Video, TokenResetPassword
from ..forms import ConfigColorsForm, PasswordResetForm
from os import path, remove
from datetime import time, timedelta
import re, secrets

from .joueur_options import *
from .login_and_out import *
from .accueil import *
from .gestionnaire_erreur import *


validate_mail_regexp = re.compile('^[0-9a-zA-Z.-_]{3,}@[0-9a-zA-Z-_]{2,}\.[a-zA-Z0-9]{2,}$')
log_dir = '/var/log/nginx/'
log_file = 'user_connections.log'


@gestionnaire_erreur
def index(request):
    if request.user.is_authenticated:
        return redirect('jeux:accueil')
    else:
        return render(request, 'jeux/index.html',
                      {'jeux': Jeu.objects.all()})

@login_required(login_url='/')
@gestionnaire_erreur
def config(request):
    form_colors = ConfigColorsForm(
        instance=Joueur.objects.get(utilisateur=request.user.id))
    password_validators = ''
    for p in password_validation.password_validators_help_texts():
        password_validators += gettext(p) + '\\n'
    return render(request, 'jeux/config.html',
                  {'colors': joueur_colors(request.user.id), 'form_colors': form_colors, 'background_image': joueur_background(request),
                   'password_validators': re.sub(r'\'', "\\'", password_validators)})


@gestionnaire_erreur
def change_info(request):
    if request.user.check_password(request.POST.get('password')) and request.method == 'POST':
        if request.POST.get('password_new_1') != request.POST.get('password_new_1'):
            request.session['error_message'] += "Les nouveaux mots de passe ne correspondent pas.\\n"
            request.session['error_not_seen'] = True
        elif not request.POST.get('password_new_1') == "" and password_validation.validate_password(request.POST.get('password')) is None:
            request.user.set_password(request.POST.get('password_new_1'))
            login(request, authenticate(
                request, username=request.user.username, password=request.POST.get('password')))
            request.user.save()
            request.session['error_message'] += "Mot de passe changé.\\n"
            request.session['error_not_seen'] = True
            print("Mot de passe changé pour " + request.user.username)
        elif request.POST.get('password_new_1') != "" and password_validation.validate_password(request.POST.get('password')) is not None:
            request.session['error_message'] += "Nouveau mot de passe incorrect.\\n"
            request.session['error_not_seen'] = True
        if validate_mail_regexp.match(request.POST.get('email')) and request.POST.get('email') != request.user.email:
            request.user.email = request.POST.get('email')
            request.user.save()
            request.session['error_message'] += "Addresse email changée.\\n"
            request.session['error_not_seen'] = True
            print('Changement de mail pour ' + request.user.username)
        elif request.POST.get('email') != request.user.email:
            request.session['error_message'] += "Addresse email incorrecte.\\n"
            request.session['error_not_seen'] = True

        form = ConfigColorsForm(request.POST, request.FILES, instance=Joueur.objects.get(
            utilisateur=request.user.id))
        if form.is_valid():
            form.clean()
            # On supprimme le fond decran si upload d'un nouveau ou demande de le supprimmer !!
            try:
                if (not form.cleaned_data['background_file'] or
                        not ('user_' + str(request.user.id) + '/') in str(form.cleaned_data['background_file'])):
                    remove(path.join(settings.MEDIA_ROOT, Joueur.objects.get(
                           utilisateur=request.user.id).background_file.name))
            except Exception as e:
                print("Error : " + str(e))
            form.save()

        return redirect('jeux:config')
    else:
        request.session['error_message'] += "Mot de passe actuel incorrect.\\n"
        request.session['error_not_seen'] = True
        return redirect('jeux:config')


def reset_password(request):
    if request.method == 'POST':
        if request.POST.get('email'):
            print('Email : ' + request.POST.get('email'))
            try:
                user_concerned = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                return HttpResponse(200)
        else:
            print('Nom d\'utilisateur : ' + request.POST.get('username'))
            try:
                user_concerned = User.objects.get(username=request.POST.get('username'))
            except User.DoesNotExist:
                return HttpResponse(200)
        print('Utilisateur trouvé.')
        try:
            dt = TokenResetPassword.objects.get(utilisateur_id=user_concerned)
            if(timezone.now() - dt.created > timedelta(minutes=15)):
                dt.delete()
            else:
                return HttpResponse(200)
        except TokenResetPassword.DoesNotExist:
            pass
        token = secrets.token_urlsafe(32)
        database_line = TokenResetPassword(utilisateur_id=user_concerned, token=token)
        database_line.save()
        message_txt = f"Salut {user_concerned.username}, \nVoici le lien de reset de ton mot de passe : \n\
                        https://malfeitor.duckdns.org/reset_page?token={token}\nSi tu n'a pas demandé ce mail merci de me le faire savoir.\nDes bisous, l'équipe d'AQuoiQuonJoue."
        message_html = f"<h2>Salut {user_concerned.username},</h2></br><a href='https://malfeitor.duckdns.org/reset_page?token={token}'>Voici le lien de reset de ton mot de passe</a>\
                        </br>Si tu n'a pas demandé ce mail merci de me le faire savoir.</br>Des bisous, l'équipe d'AQuoiQuonJoue."
        send_mail('[AQuoiQuonJoue] Demande de réinitialisation de mot de passe.', message_txt,
                  'aquoiquonjoue@malfeitor.duckdns.org', [user_concerned.email], html_message=message_html)
        return HttpResponse(200)
    return redirect('jeux:index')


@gestionnaire_erreur
def reset_page(request):
    if request.method == 'GET':
        password_validators = ''
        for p in password_validation.password_validators_help_texts():
            password_validators += gettext(p) + '\\n'
        try:
            token = request.GET.get('token', False)
            token = TokenResetPassword.objects.get(token=token)
            if(timezone.now() - token.created > timedelta(minutes=15)):
                token.delete()
                request.session['error_message'] += "Trop tard, token périmé, essaie encore.\\n"
                request.session['error_not_seen'] = True
                return redirect('jeux:index')
            else:
                form = PasswordResetForm()
                return render(request, 'jeux/password_reset.html', {'form': form, 'password_validators': re.sub(r'\'', "\\'", password_validators),
                                                                    'token': token.token})

        except TokenResetPassword.DoesNotExist:
            request.session['error_message'] += "Le token n'existe pas.\\n"
            request.session['error_not_seen'] = True
            return redirect('jeux:index')
    elif request.method == 'POST':
        password_validators = ''
        for p in password_validation.password_validators_help_texts():
            password_validators += gettext(p) + '\\n'
        token_post = request.POST.get('token')
        print(token_post)
        pass_1 = request.POST.get('new_password_1')
        pass_2 = request.POST.get('new_password_2')
        if pass_1 != pass_2:
            request.session['error_message'] += "Les mots de passe sont différents.\\n"
            request.session['error_not_seen'] = True
            form = PasswordResetForm()
            return render(request, 'jeux/password_reset.html', {'form': form, 'password_validators': re.sub(r'\'', "\\'", password_validators),
                                                                'token': token_post})
        try:
            if password_validation.validate_password(pass_1) is None:
                try:
                    token = TokenResetPassword.objects.get(token=token_post)
                    if(timezone.now() - token.created > timedelta(minutes=15)):
                        token.delete()
                        return redirect('jeux:index')
                    user = token.utilisateur_id
                    user.set_password(pass_1)
                    user.save()
                    login(request, authenticate(
                          request, username=token.utilisateur_id.username, password=pass_1))
                    token.delete()
                    print('Mdp de ' + user.username + ' changé.')
                    request.session['error_message'] += "Mot de passe changé.\\n"
                    request.session['error_not_seen'] = True
                    return redirect('jeux:index')
                except TokenResetPassword.DoesNotExist:
                    return redirect('jeux:accueil')
        except password_validation.ValidationError as e:
            for message in e:
                request.session['error_message'] += message + "\\n"
            request.session['error_not_seen'] = True
            form = PasswordResetForm()
            return render(request, 'jeux/password_reset.html', {'form': form, 'password_validators': re.sub(r'\'', "\\'", password_validators),
                                                                'token': token_post})
    return render(request, 'jeux/index.html')


@login_required(login_url='/')
@gestionnaire_erreur
def mes_amis(request):
    return render(request, 'jeux/mes_amis.html',
                  {'colors': joueur_colors(request.user.id), 'background_image': joueur_background(request)})


@login_required(login_url='/')
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
                if possesseur.utilisateur.username not in liste_possesseurs_amis:
                    liste_possesseurs_amis.append(
                        possesseur.utilisateur.username)
        if len(liste_jeux[jeu.id]['possede_par']) == 0:
            liste_jeux.pop(jeu.id, None)
    return render(request, 'jeux/jeux_societe.html',
                  {'jeux': liste_jeux, 'possesseurs_amis': liste_possesseurs_amis,
                   'colors': joueur_colors(request.user.id), 'amis': liste_amis, 'background_image': joueur_background(request)})


@login_required(login_url='/')
def ajouter_jeu_societe_bdd(request):
    if (int(request.POST.get('joueurs_min')) >= 1 and int(request.POST.get('joueurs_max')) >= 2 and
        len(request.POST.get('nom')) >= 4 and len(request.POST.get('nom')) < 50 and
            (int(request.POST.get('temps_prevu_h')) >= 0 and int(request.POST.get('temps_prevu_min')) >= 0)):
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
