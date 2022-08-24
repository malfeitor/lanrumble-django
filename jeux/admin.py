from django.contrib import admin
from .models import Jeu, Joueur, Jeu_Societe, Vote_Jeu_Video, TokenResetPassword


class Jeu_SocieteAdmin(admin.ModelAdmin):
    list_display = ("nom", "temps_prevu", "joueurs_min", "joueurs_max")


class JeuAdmin(admin.ModelAdmin):
    list_display = ("nom", "coop", "pvp", "f2p", "joueurs_max_online",
                    "joueurs_max_hot_seat")


admin.site.register(Jeu, JeuAdmin)
admin.site.register(Joueur)
admin.site.register(Jeu_Societe, Jeu_SocieteAdmin)
admin.site.register(Vote_Jeu_Video)
admin.site.register(TokenResetPassword)
