from django.shortcuts import render
from rest_framework import generics
from restApi.models import Utilisateur, Voiture, Utilisateur_loue_voiture
from restApi.serializers import VoitureSerializer, UtilisateurSerializer, ULVSerializer
# Create your views here.

class VoitureCreateView(generics.CreateAPIView):
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer

class UtilisateurCreateView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class ULVCreateView(generics.CreateAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer