from ..models import Player


def joueur_colors(joueur_id):
    """Fonction pour avoir la liste des couleurs de l'utilisateur logé"""
    try:
        joueur = Player.objects.get(user=joueur_id)
    except Exception as e:
        print(e)
    return {
        "body_background": joueur.color_body_background,
        "body_text": joueur.color_body_text,
        "nav_background": joueur.color_nav_background,
        "nav_link_active": joueur.color_nav_link_active,
        "nav_link_hover": joueur.color_nav_link_hover,
        "nav_link": joueur.color_nav_link,
        "nav_text": joueur.color_nav_text,
    }


def joueur_background(request):
    """Fonction pour avoir le fond d'écran de l'utilisateur logé"""
    try:
        background_image = Player.objects.get(user=request.user.id).background_file.url
    except Exception:
        background_image = ""
    return background_image
