from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from restApi.models import Utilisateur, Voiture, Utilisateur_loue_voiture, Parametres_voiture
from restApi.serializers import FullVoitureSerializer, ConsoVoitureSerializer, FullUtilisateurSerializer, ULVSerializer, CreationOTPSerializer, VerifyOTPSerializer, ParametresVoitureSerializer
# Create your views here.

"""
    Post Handling views
"""

class VoitureCreateView(generics.CreateAPIView):
    queryset = Voiture.objects.all()
    serializer_class = FullVoitureSerializer

    def create(self,request,*args,**kwargs):
        param = request.data['parametres_voiture']
        try:
            para_id = Parametres_voiture.objects.get(nom_modele=param).param_id
        except Parametres_voiture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.data["parametres_voiture"] = para_id
        return super(VoitureCreateView,self).create(request,*args,**kwargs)

class UtilisateurCreateView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = FullUtilisateurSerializer

class ULVCreateView(generics.CreateAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer

    def create(self,request,*args,**kwargs):
        mat = request.data["voiture"]
        try:
            voit_id = Voiture.objects.get(matricule=mat).car_id
        except Voiture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.data["voiture"] = voit_id
        return super(ULVCreateView,self).create(request,*args,**kwargs)

class OTPCreationView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = CreationOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer_instance = self.get_serializer(data=request.data)
        serializer_instance.is_valid(raise_exception=True)
        reponse = serializer_instance.save()
        headers = self.get_success_headers(serializer_instance.data)
        return Response(reponse, status=status.HTTP_200_OK,headers=headers)



class OTPVerifyView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = VerifyOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer_instance = self.get_serializer(data=request.data)
        serializer_instance.is_valid(raise_exception=True)
        reponse = serializer_instance.save()
        headers = self.get_success_headers(serializer_instance.data)
        return Response(reponse, status=status.HTTP_200_OK,headers=headers)

"""
    Get Handling Views
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

class ParametresRetriveView(generics.RetrieveAPIView):
    queryset = Voiture.objects.all()
    serializer_class = ParametresVoitureSerializer
    lookup_field = 'matricule'

"""
    Update Handling Views
"""
class FullVoitureUDView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Voiture.objects.all()
    serializer_class = FullVoitureSerializer
    lookup_field = 'matricule'

    def update(self,request,*args,**kwargs):
        param = request.data["parametres_voiture"]
        try:
            param_id = Parametres_voiture.objects.get(nom_modele=param).param_id
        except Parametres_voiture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.data["parametres_voiture"] = param_id
        return super(FullVoitureUDView,self).update(request,*args,**kwargs)


"""
DELETE Handling Views
"""
class ULVDestroyView(generics.DestroyAPIView):
    queryset = Utilisateur_loue_voiture.objects.all()
    serializer_class = ULVSerializer
    lookup_field = 'ulv_id'
