#!/usr/bin/python3
from django.core.management.base import BaseCommand, CommandError

from jeux.models import Videogame, Player, VideogameRating


class Command(BaseCommand):
    help = "Usage : \najout_f2p   -> give F2P games to all users.\nset_vote_5  -> set ALL votes to 5 !"

    def add_arguments(self, parser):
        parser.add_argument("Args", nargs="+", type=int)

    def handle(self, *args, **options):
        if "ajout_f2p" not in options["Args"] and "set_vote_5" not in options["Args"]:
            print(
                "Usage : \najout_f2p   -> give F2P games to all users.\nset_vote_5  -> set ALL votes to 5 !"
            )
            return
        jeux_presents = Videogame.objects.all()
        joueurs_presents = Player.objects.all()
        if "ajout_f2p" in options["Args"]:
            for i in joueurs_presents:
                for j in jeux_presents:
                    if j not in i.videogames_list.all():
                        i.videogames_list.add(j)
                        i.save()
        if "set_vote_5" in options["Args"]:
            for i in joueurs_presents:
                for j in jeux_presents:
                    VideogameRating(jeu_concerne=j, joueur_concerne=i, valeur=5).save()
        self.stdout.write(self.style.SUCCESS("JOB DONE !"))
