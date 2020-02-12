#!/usr/bin/python3
from django.core.management.base import BaseCommand, CommandError

from jeux.models import Jeu, Joueur, Vote_Jeu_Video


class Command(BaseCommand):
    help = 'Usage : \najout_f2p   -> give F2P games to all users.\nset_vote_5  -> set ALL votes to 5 !'

    def add_arguments(self, parser):
        parser.add_argument('Args', nargs='+', type=int)

    def handle(self, *args, **options):
        if not "ajout_f2p" in options['Args'] and not "set_vote_5" in options['Args']:
            print('Usage : \najout_f2p   -> give F2P games to all users.\nset_vote_5  -> set ALL votes to 5 !')
            return
        jeux_presents = Jeu.objects.all()
        joueurs_presents = Joueur.objects.all()
        if "ajout_f2p" in options['Args']:
            for i in joueurs_presents:
                for j in jeux_presents:
                    if not j in i.liste_jeux.all():
                        i.liste_jeux.add(j)
                        i.save()
        if "set_vote_5" in options['Args']:
            for i in joueurs_presents:
                for j in jeux_presents:
                    Vote_Jeu_Video(jeu_concerne=j, joueur_concerne=i, valeur=5).save()
        self.stdout.write(self.style.SUCCESS('JOB DONE !'))
