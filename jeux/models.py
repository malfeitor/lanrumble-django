from django.db import models
from django.contrib.auth.models import User
from datetime import time


class Videogame(models.Model):
    title = models.CharField(max_length=100, unique=True)
    coop = models.BooleanField(default=False)
    pvp = models.BooleanField(default=False)
    max_hot_seat_players = models.SmallIntegerField(default=1)
    max_online_players = models.SmallIntegerField(default=0)
    f2p = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.utilisateur_id, filename)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", blank=True)
    videogames_list = models.ManyToManyField(Videogame, blank=True)
    color_body_background = models.CharField(max_length=7, default="#222222")
    color_body_text = models.CharField(max_length=7, default="#ffffff")
    color_nav_background = models.CharField(max_length=7, default="#111111")
    color_nav_link_active = models.CharField(max_length=7, default="#ff0000")
    color_nav_link_hover = models.CharField(max_length=7, default="#ffffff")
    color_nav_link = models.CharField(max_length=7, default="#990000")
    color_nav_text = models.CharField(max_length=7, default="#ffffff")
    background_file = models.FileField(upload_to=user_directory_path, blank=True)

    objects = models.Manager()
    delete_files = models.Manager()

    def __str__(self):
        return self.user.username


class Boardgame(models.Model):
    title = models.CharField(max_length=100, unique=True)
    game_time = models.TimeField(default=time(1, 1))
    max_players = models.SmallIntegerField(default=1)
    min_players = models.SmallIntegerField(default=1)
    difficulty = models.SmallIntegerField(default=1)
    owned_by = models.ManyToManyField(Player, blank=True)

    def __str__(self):
        return self.title


class VideogameRating(models.Model):
    rating = models.SmallIntegerField(default=5)
    videogame = models.ForeignKey(
        Videogame,
        blank=False,
        on_delete=models.CASCADE,
        db_column="jeu_concerne",
    )
    player = models.ForeignKey(
        Player,
        blank=False,
        on_delete=models.CASCADE,
        db_column="joueur_concerne",
    )

    def __str__(self):
        return (
            self.player.user.username
            + " - "
            + self.videogame.title
            + " = "
            + str(self.rating)
        )


class TokenResetPassword(models.Model):
    utilisateur_id = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            self.utilisateur_id.username
            + " @ "
            + self.created.strftime("%d/%m/%Y %H:%M:%S")
            + " UTC"
        )
