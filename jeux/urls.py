from django.urls import path
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "jeux"
urlpatterns = [
    path("", views.index, name="index"),
    path("loginside", views.loginside, name="loginside"),
    path("logoutside", views.logoutside, name="logoutside"),
    path("accueil", views.accueil, name="accueil"),
    path("config", views.config, name="config"),
    path("change_info", views.change_info, name="change_info"),
    path("mes_jeux", views.mes_jeux, name="mes_jeux"),
    path("mes_jeux_ajouter", views.mes_jeux_ajouter, name="mes_jeux_ajouter"),
    path("mes_jeux_enlever", views.mes_jeux_enlever, name="mes_jeux_enlever"),
    path("ajouter_jeu_bdd", views.ajouter_jeu_bdd, name="ajouter_jeu_bdd"),
    path("mes_amis", views.mes_amis, name="mes_amis"),
    path("ajax/vote_jeuvideo", views.ajax_vote_videogame, name="ajax_vote_videogame"),
    path("jeux_societe", views.jeux_societe, name="jeux_societe"),
    path(
        "ajouter_jeu_societe_bdd",
        views.ajouter_jeu_societe_bdd,
        name="ajouter_jeu_societe_bdd",
    ),
    path("reset_password", views.reset_password, name="reset_password"),
    path("reset_page", views.reset_page, name="reset_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    handler400 = "jeux.views.bad_request"
    handler403 = "jeux.views.permission_denied"
    handler404 = "jeux.views.page_not_found"
    handler500 = "jeux.views.server_error"
