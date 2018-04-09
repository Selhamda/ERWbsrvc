from rest_framework import serializers
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture

class ULVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur_loue_voiture
        fields = ('utilisateur','voiture','consommation','date_transaction','ulv_id')
        read_only_fields = ('date_transaction','ulv_id')
        extra_kwargs = {'voiture': {'write_only': True}}
    
    def create(self,validated_data):
        #get id utilisateur et voiture et cherher des correspondance dans la bdd pour creer
        user = validated_data.pop('utilisateur')
        car= validated_data.pop('voiture')
        ulv = Utilisateur_loue_voiture.objects.create(utilisateur=user,voiture=car,**validated_data)
        return ulv
    
    def update(self, instance, validated_data):
        #maj conso sur la carte ulv
        instance.consommation = validated_data.get('consommation')
        return instance

class ParametresVoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres_voiture
        fields = ('parametre_1', 'parametre_2','date_modif')
        read_only_fields = ('date_modif',)

class FullVoitureSerializer(serializers.ModelSerializer):
    parametres_voiture = ParametresVoitureSerializer()
    users_set = ULVSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Voiture
        fields = ('car_id','nom_modele','proprietaire', 'parametres_voiture', 'users_set', 'date_creation', 'date_modif')
        read_only_fields = ('car_id','date_creation', 'date_modif')

    def validate(self, data):
        try:
            car = Voiture.objects.get(car_id=data['car_id'])
            if car is not None:
                owner = car.proprietaire
                if owner.user_id != data['proprietaire']:
                    raise serializers.ValidationError("Must be car owner to proceed")
            return data
        except KeyError:
            return data
        
        

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
    users_set = users_set = ULVSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Voiture
        fields = ('car_id','nom_modele', 'users_set')
        read_only_fields = ('car_id',)

class BasicVoitureSerializer(serializers.ModelSerializer):

        class Meta:
            model = Voiture
            fields = ('car_id','nom_modele','date_creation')
            read_only_fields = ('car_id','date_creation')

class FullUtilisateurSerializer(serializers.ModelSerializer):
    owned_set = BasicVoitureSerializer(many=True,required=False,read_only=True)
    class Meta:
        #class meta lie les champs du serializer avec ceux du model
        model = Utilisateur
        fields = ('user_id','nom' ,'owned_set', 'date_creation', 'date_modif')
        read_only_fields = ('user_id','date_creation', 'date_modif')