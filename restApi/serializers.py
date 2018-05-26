from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture
from .validators import matricule_syntax, ConsoFloatValidator


class ULVSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utilisateur_loue_voiture
        fields = ('utilisateur','nom','voiture','consommation','date_transaction','ulv_id','titre_conso')
        read_only_fields = ('date_transaction','ulv_id')
        extra_kwargs = {
            'voiture': {'write_only': True},
            'consommation': {
                'validators':[ConsoFloatValidator(field='consommation')]
            }
        }

    def create(self,validated_data):
        #get id utilisateur et voiture et cherher des correspondance dans la bdd pour creer
        user = validated_data.pop('utilisateur')
        car = validated_data.pop('voiture')
        ulv = Utilisateur_loue_voiture.objects.create(utilisateur=user,voiture=car,**validated_data)
        return ulv

    def update(self, instance, validated_data):
        #maj conso sur la carte ulv
        instance.consommation = validated_data.get('consommation')
        return instance

    def validate(self, data):
        try:
            car = data['voiture']
            util = data['utilisateur']
        except KeyError:
            raise serializers.ValidationError('Voiture and Utilisateur fields are required.')

        try:
            name = data['nom']
        except KeyError:
            raise serializers.ValidationError("nom field is required.")

        #je cree une aggregation sur la table en comptant les ulv par apparition d'un user
        ulvs = Utilisateur_loue_voiture.objects.values('utilisateur','nom').annotate(Sum('consommation'))
        #partie pour empecher un user d'utiliser un nom existant
        for ulv in ulvs:
            if ulv['utilisateur'] != util.user_id and ulv['nom'] == name:
                raise serializers.ValidationError('Selected name already exists.')

            #partie pour empecher un user de s'inscrire avec deux noms differents
            elif ulv['utilisateur'] == util.user_id and ulv['nom'] != name:
                raise serializers.ValidationError('Cannot subscribe to same car with different names')

        return super(ULVSerializer,self).validate(data)

###########
###Pour voiture
###########

class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        info = data.values('utilisateur','nom').annotate(Sum('consommation'))
        output = []
        for ulv in info:
            dico = {
                'nom' : ulv['nom'],
                'user_id' : ulv['utilisateur'],
                'solde' : ulv['consommation__sum'],
            }
            output.append(dico)
        return output

class FilteredULVSerializer(ULVSerializer):
    class Meta(ULVSerializer.Meta):
        list_serializer_class = FilteredListSerializer

class ParametresVoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres_voiture
        fields = ('parametre_1', 'parametre_2','date_modif')
        read_only_fields = ('date_modif',)

class FullVoitureSerializer(serializers.ModelSerializer):
    parametres_voiture = ParametresVoitureSerializer()
    users_set = FilteredULVSerializer(
        many=True,
        required=False,
        read_only=True
    )
    class Meta:
        model = Voiture
        fields = ('matricule','nom_modele','proprietaire', 'parametres_voiture', 'users_set', 'date_creation', 'date_modif')
        read_only_fields = ('date_creation', 'date_modif')
        extra_kwargs = {
            'matricule': {
                'validators': [UniqueValidator(Voiture.objects.all()), matricule_syntax]
            }
        }


    def create(self, validated_data):
        parametres_data = validated_data.pop('parametres_voiture')
        owner = validated_data.pop('proprietaire')
        voiture = Voiture.objects.create(proprietaire=owner,**validated_data)
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

class ConsoVoitureSerializer(serializers.ModelSerializer):
    users_set = ULVSerializer(
        many=True,
        required=False,
        read_only=True
    )
    class Meta:
        model = Voiture
        fields = ('matricule','nom_modele', 'users_set')
        read_only_fields = ('matricule',)

###########
###Pour utilisateur
###########

class BasicVoitureSerializer(serializers.ModelSerializer):

        class Meta:
            model = Voiture
            fields = ('matricule','nom_modele','date_creation')
            read_only_fields = ('matricule','date_creation')

class UserListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        info = data.values('utilisateur','voiture').annotate(Sum('consommation'))
        output = []
        for ulv in info:
            voit = Voiture.objects.get(car_id=ulv['voiture'])
            matri = voit.matricule
            name = voit.nom_modele
            dico = {
                'matricule' : matri,
                'nom' : name,
            }
            output.append(dico)
        return output

class UserULVSerializer(ULVSerializer):
    class Meta(ULVSerializer.Meta):
        list_serializer_class = UserListSerializer

class FullUtilisateurSerializer(serializers.ModelSerializer):
    owned_set = BasicVoitureSerializer(
        many=True,
        required=False,
        read_only=True
    )
    cars_set = UserULVSerializer(
        many=True,
        required=False,
        read_only=True
    )
    class Meta:
        #class meta lie les champs du serializer avec ceux du model
        model = Utilisateur
        fields = ('user_id','owned_set','cars_set', 'date_creation', 'date_modif')
        read_only_fields = ('user_id','date_creation', 'date_modif')

###########
###Pour recup compte
###########
