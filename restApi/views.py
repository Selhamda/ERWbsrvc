from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import get_object_or_404
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

class VoitureRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer
    lookup_field = 'car_id'

class UtilisateurRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    lookup_field = 'user_id'

class ULVRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer
    multiple_lookup_fields = ('utilisateur','voiture')

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        return obj

