from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture
from .validators import matricule_syntax, ConsoFloatValidator
from django.core.mail import send_mail
from django.template.loader import render_to_string
import pyotp

class ULVSerializer(serializers.ModelSerializer):
    """
        Serializer pour le modele Utilisateur_loue_voiture
    """
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
    """
        Chargement de la methode to_representation de ListSerializer pour
        customiser le comportement du serializer quand on choisit many = True
        a savoir comment le serializer manie les relations to many
        Objectif : aggreger les ulvs selon une somme des consos pour chaque utilisateur
    """
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
    """
        Serializer dont on veut changer le comportement
    """
    class Meta(ULVSerializer.Meta):
        list_serializer_class = FilteredListSerializer

class ParametresVoitureSerializer(serializers.ModelSerializer):
    """
        pour get les parametres d'une voiture specifique
    """
    class Meta:
        model = Voiture
        fields = ('parametres_voiture',)
        read_only_fields ={'parametres_voiture',}

class FullVoitureSerializer(serializers.ModelSerializer):
    """
        Principal serializer pour le modele voiture
        users_set : utilisateurs inscrits à la voiture et leur conso totale
    """
    users_set = FilteredULVSerializer(
        many=True,
        required=False,
        read_only=True
    )
    nom_proprietaire = serializers.CharField(write_only=True)

    class Meta:
        model = Voiture
        fields = ('matricule','proprietaire','nom_proprietaire', 'parametres_voiture', 'users_set', 'date_creation', 'date_modif')
        read_only_fields = ('date_creation', 'date_modif')
        extra_kwargs = {
            'matricule': {'validators': [UniqueValidator(Voiture.objects.all()), matricule_syntax]},
            'parametres_voiture': {'write_only' : True,},
        }


    def create(self, validated_data):
        parametres = validated_data.pop('parametres_voiture')
        owner = validated_data.pop('proprietaire')
        name = validated_data.pop('nom_proprietaire')
        voiture = Voiture.objects.create(proprietaire=owner,parametres_voiture=parametres, **validated_data)
        Utilisateur_loue_voiture.objects.create(voiture=voiture, utilisateur=owner, nom=name)
        return voiture

    def update(self, instance, validated_data):
        parametres_data = validated_data.get('parametres_voiture')
        if parametres_data is not None:
            instance.parametres_voiture = parametres_data
        return instance

class ConsoVoitureSerializer(serializers.ModelSerializer):
    """
        Modele utilise pour visualiser les details de toutes les transactions
    """
    users_set = ULVSerializer(
        many=True,
        required=False,
        read_only=True
    )
    class Meta:
        model = Voiture
        fields = ('matricule', 'users_set')
        read_only_fields = ('matricule',)

###########
###Pour utilisateur
###########

class BasicVoitureSerializer(serializers.ModelSerializer):
    """
        Serializer pour rappeler les caracterstiques principales de la voiture
        possedee
    """

    class Meta:
        model = Voiture
        fields = ('matricule', 'date_creation')
        read_only_fields = ('matricule','date_creation')

class UserListSerializer(serializers.ListSerializer):
    """
        Objectif : Aggreger les ulvs de sorte à avoir toutes les voitures
        auxquelles un utilisateur est inscrit.
    """
    def to_representation(self, data):
        info = data.values('utilisateur','voiture').annotate(Sum('consommation'))
        output = []
        for ulv in info:
            voit = Voiture.objects.get(car_id=ulv['voiture'])
            matri = voit.matricule
            name = voit.parametres_voiture.nom_modele
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
    """
        Principal serializer pour le modele Utilisateur
        owned_set : voitures possedees
        cars_set : voitures auxquelles l'utilisateur est inscrit
    """
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
        #class meta lie les champs du serializer avec ceux du modele
        model = Utilisateur
        fields = ('user_id', 'email', 'owned_set', 'cars_set', 'date_creation', 'date_modif')
        read_only_fields = ('user_id','date_creation', 'date_modif')
        extra_kwargs = {
            'email':{
                'validators':[UniqueValidator(Utilisateur.objects.all())]
            }
        }

###########
###Pour recup compte
###########

class OTPSerializer(serializers.ModelSerializer):
    """
        Serializer en commun pour creation et verification d'otp
        pour factorisation de code

    """
    interval = 300

    class Meta:
        model = Utilisateur
        fields = ('email',)

    def validate(self, data):
        val_data = super(OTPSerializer,self).validate(data)
        try:
            uzr = Utilisateur.objects.get(email=val_data['email'])
            val_data.update({'user' : uzr})
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError('no user registered with such email address')
        return val_data

class CreationOTPSerializer(OTPSerializer):
    """
        Serializer pour creation des otps (one time passwords) selon un critere de temps
        et de l'envoi des emails

    """

    class Meta(OTPSerializer.Meta):
        model = Utilisateur

    def save(self):
        """
            creation des topt (time based otp) necessite un intervalle de validite.
            Les standards de l'algo recommandent 30s si les clocks sont synchro on prend 2x plus pour la marge

        """
        #generation de l'otp
        user = self.validated_data['user']
        base32str = user.secret
        totp = pyotp.TOTP(base32str, interval=self.interval)
        otp = totp.now()

        #envoi de l'email
        subject = 'Account retrieval'
        dico = {
            'app_name' : 'EasyRide',
            'code' : otp,
        }
        message = render_to_string('reset_email.html',dico)
        recipient = self.validated_data['email']
        sender = 'reset@easyride'
        send_mail(
            subject,
            message,
            sender,
            [recipient],
            fail_silently=False,
        )

        #synthese de la reponse
        reponse = {
            #'otp' : dico['code'],
            'message':'retrieval password successfully sent',
            }

        return reponse

class VerifyOTPSerializer(OTPSerializer):
    """
        Pour verification des otps

    """
    otp = serializers.CharField(required=True)

    class Meta(OTPSerializer.Meta):
        model = Utilisateur
        fields = ('otp','email')

    def save(self):
        otp = self.validated_data['otp']
        user_secret = self.validated_data['user'].secret
        totp = pyotp.TOTP(user_secret, interval=self.interval)
        if totp.verify(otp):
            reponse = {
                'user_id' : self.validated_data['user'].user_id,
            }
            return reponse
        else:
            reponse = {
                'message' : 'One time password does not match'
            }
            return reponse
