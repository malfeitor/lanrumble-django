from django.shortcuts import render
from rest_framework import viewsets
from ..serializers import JeuSerializer
from ..models import Jeu

class JeuxView(viewsets.ModelViewSet):
	serializer_class = JeuSerializer
	queryset = Jeu.objects.all()