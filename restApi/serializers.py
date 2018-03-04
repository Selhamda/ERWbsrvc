from rest_framework import serializers
from .models import *

class ULVSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('utilisateur','voiture','consommation','date_debut_location', 'date_fin_location')
        read_only_fields = ('date_debut_location', 'date_fin_location')
        depth = 1

class UtilisateurSerializer(serializers.ModelSerializer):
    voitures = ULVSerializer(many=True)
    class Meta:
        "class meta lie les champs du serializer avec ceux du model"
        model = Utilisateur
        fields = ('nom' ,'voitures', 'date_creation', 'date_modif')
        read_only_fields = ('date_creation', 'date_modif','voitures')

class ParametresVoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres_voiture
        fields = ('parametre_1', 'parametre_2','date_modif')
        read_only_fields = ('date_modif',)

class VoitureSerializer(serializers.ModelSerializer):
    parametres_voiture = ParametresVoitureSerializer()
    utilisateurs = ULVSerializer(many=True)
    class Meta:
        model = Voiture
        fields = ('nom_modele', 'parametres_voiture', 'utilisateurs', 'date_creation', 'date_modif')
        read_only_fields = ('date_creation', 'date_modif','utilisateurs')

    def create(self, validated_data):
        parametres_data = validated_data.pop('parametres_voiture')
        voiture = Voiture.objects.create(**validated_data)
        parametres_voiture = Parametres_voiture.objects.create(voiture=voiture,**parametres_data)
        return voiture
    
    def update(self, instance, validated_data):
        parametres_data = validated_data.get('parametres_voiture')
        instance.parametres_voiture.parametre_1 = parametres_data.get('parametre_1')
        instance.parametres_voiture.parametre_2 = parametres_data.get('parametre_2')
        instance.nom_modele = validated_data.get('nom_modele')
        return instance
