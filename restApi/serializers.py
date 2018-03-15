from rest_framework import serializers
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture

class ULVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur_loue_voiture
        fields = ('utilisateur','voiture','consommation','date_debut_location', 'date_fin_location')
        read_only_fields = ('date_debut_location', 'date_fin_location')
    
    def create(self,validated_data):
        #get id utilisateur et voiture et cherher des correspondance dans la bdd pour creer
        user = validated_data.pop('utilisateur')
        #user = Utilisateur.objects.get(user_id=user_id)
        car= validated_data.pop('voiture')
        #car = Voiture.objects.get(car_id=car_id)
        ulv = Utilisateur_loue_voiture.objects.create(utilisateur=user,voiture=car,**validated_data)
        return ulv
    
    def update(self, instance, validated_data):
        #maj conso sur la carte ulv
        instance.consommation = validated_data.get('consommation')
        return instance


class UtilisateurSerializer(serializers.ModelSerializer):
    cars_set = ULVSerializer(many=True,required=False)
    class Meta:
        #class meta lie les champs du serializer avec ceux du model
        model = Utilisateur
        fields = ('user_id','nom' ,'cars_set', 'date_creation', 'date_modif')
        read_only_fields = ('user_id','date_creation', 'date_modif','cars_set')

class ParametresVoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres_voiture
        fields = ('parametre_1', 'parametre_2','date_modif')
        read_only_fields = ('date_modif',)

class VoitureSerializer(serializers.ModelSerializer):
    parametres_voiture = ParametresVoitureSerializer()
    users_set = ULVSerializer(many=True,required=False)
    class Meta:
        model = Voiture
        fields = ('car_id','nom_modele', 'parametres_voiture', 'users_set', 'date_creation', 'date_modif')
        read_only_fields = ('car_id','date_creation', 'date_modif','users_set')

    def create(self, validated_data):
        parametres_data = validated_data.pop('parametres_voiture')
        voiture = Voiture.objects.create(**validated_data)
        Parametres_voiture.objects.create(voiture=voiture,**parametres_data)
        return voiture
    
    def update(self, instance, validated_data):
        parametres_data = validated_data.get('parametres_voiture')
        new_param_1 = parametres_data.get('parametre_1')
        if new_param_1 is not None:
            instance.parametres_voiture.parametre_1 = new_param_1
        new_param_2 = parametres_data.get('parametre_2')
        if new_param_2 is not None:
            instance.parametres_voiture.parametre_2 = new_param_2
        new_model_name = validated_data.get('nom_modele')
        if new_model_name is not None:
            instance.nom_modele = new_model_name 
        return instance
