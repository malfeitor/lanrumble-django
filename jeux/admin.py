from django.contrib import admin
from .models import Jeu, Joueur, Jeu_Societe, Vote_Jeu_Video, TokenResetPassword


admin.site.register(Jeu)
admin.site.register(Joueur)
admin.site.register(Jeu_Societe)
admin.site.register(Vote_Jeu_Video)
admin.site.register(TokenResetPassword)
