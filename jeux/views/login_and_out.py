from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from os import path
from ..models import Jeu, Joueur


log_dir = '/var/log/nginx/'
log_file = 'user_connections.log'


def loginside(request):
    """Vue de connection"""
    pseud = request.POST.get('pseudo')
    passwd = request.POST.get('password')
    user = authenticate(request, username=pseud, password=passwd)
    if user is not None:
        login(request, user)
    else:
        with open(path.join(log_dir, log_file), 'a') as log_file_opened:
            log_file_opened.write(request.META['HTTP_X_REAL_IP'] + ' - ' +
                                  timezone.now().strftime("%Y/%m/%d %H:%M:%S +%Z") + ' - ' + pseud + '\n')
        request.session['error_message'] += 'Login ou mot de passe incorrect.\\n'
        request.session['error_not_seen'] = True
        return redirect('jeux:index')
    try:
        joueur = Joueur.objects.get(utilisateur=user.id)
        joueur.utilisateur.check_password(passwd)
    except Exception:
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