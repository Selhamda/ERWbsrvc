from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import get_object_or_404
from restApi.models import Utilisateur, Voiture, Utilisateur_loue_voiture
from restApi.serializers import FullVoitureSerializer, ConsoVoitureSerializer, FullUtilisateurSerializer, ULVSerializer
# Create your views here.

"""
POST Handling views
"""

class VoitureCreateView(generics.CreateAPIView):
    queryset = Voiture.objects.all()
    serializer_class = FullVoitureSerializer

class UtilisateurCreateView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = FullUtilisateurSerializer

class ULVCreateView(generics.CreateAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer

    def create(self,request,*args,**kwargs):
        mat = request.data["voiture"]
        voit_id = Voiture.objects.get(matricule=mat).car_id
        request.data["voiture"] = voit_id
        return super(ULVCreateView,self).create(request,*args,**kwargs)

"""    
GET Handling Views
"""

class FullVoitureRetrieveView(generics.RetrieveAPIView):
    queryset = Voiture.objects.all()
    serializer_class = FullVoitureSerializer
    lookup_field = 'matricule'


class ConsoVoitureRetrieveView(generics.RetrieveAPIView):
    queryset = Voiture.objects.all()
    serializer_class = ConsoVoitureSerializer
    lookup_field = 'matricule'


class UtilisateurRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Also handles update and destroy"""
    queryset = Utilisateur.objects.all()
    serializer_class = FullUtilisateurSerializer
    lookup_field = 'user_id'

"""    
UPDATE Handling Views
"""
class FullVoitureUDView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Voiture.objects.all()
    serializer_class = FullVoitureSerializer
    lookup_field = 'matricule'

"""    
DELETE Handling Views
"""
class ULVDestroyView(generics.DestroyAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer
    lookup_field = 'ulv_id'


