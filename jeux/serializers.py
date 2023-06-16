from rest_framework import serializers
from .models import Joueur, Jeu, Jeu_Societe, Vote_Jeu_Video

class JeuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Jeu
		fields = ('id', 'nom', 'coop', 'pvp', 'joueurs_max_hot_seat', 'f2p', 'joueurs_max_online')