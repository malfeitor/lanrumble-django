from django.db import models
from django.contrib.auth.models import User
from datetime import time


class Jeu(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    coop = models.BooleanField(default=False)
    pvp = models.BooleanField(default=False)
    joueurs_max_hot_seat = models.SmallIntegerField(default=1)
    joueurs_max_online = models.SmallIntegerField(default=0)
    f2p = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.utilisateur_id, filename)


class Joueur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    amis = models.ManyToManyField("self", blank=True)
    liste_jeux = models.ManyToManyField(Jeu, blank=True)
    color_body_background = models.CharField(max_length=7, default="#222222")
    color_body_text = models.CharField(max_length=7, default="#ffffff")
    color_nav_background = models.CharField(max_length=7, default="#111111")
    color_nav_link_active = models.CharField(max_length=7, default="#ff0000")
    color_nav_link_hover = models.CharField(max_length=7, default="#ffffff")
    color_nav_link = models.CharField(max_length=7, default="#990000")
    color_nav_text = models.CharField(max_length=7, default="#ffffff")
    background_file = models.FileField(
        upload_to=user_directory_path, blank=True)

    objects = models.Manager()
    delete_files = models.Manager()

    def __str__(self):
        return self.utilisateur.username


class Jeu_Societe(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    temps_prevu = models.TimeField(default=time(1, 1))
    joueurs_max = models.SmallIntegerField(default=1)
    joueurs_min = models.SmallIntegerField(default=1)
    complexite = models.SmallIntegerField(default=1)
    possede_par = models.ManyToManyField(Joueur, blank=True)

    def __str__(self):
        return self.nom


class Vote_Jeu_Video(models.Model):
    valeur = models.SmallIntegerField(default=5)
    jeu_concerne = models.ForeignKey(Jeu, blank=False, on_delete=models.CASCADE)
    joueur_concerne = models.ForeignKey(Joueur, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.joueur_concerne.utilisateur.username + " - " + self.jeu_concerne.nom + " = " + str(self.valeur)
