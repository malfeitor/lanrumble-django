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
