from django.db import models
import uuid
import pyotp

# Create your models here.

class Utilisateur(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=254, null=True)
    secret = models.CharField(null=False, blank=False, max_length=50, default=pyotp.random_base32())

    def __str__(self):
        return "{{\n \t user_id : {},\n \t ajouté le : {}\n}}".format(self.user_id, self.date_creation)

class Voiture(models.Model):
    car_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietaire = models.ForeignKey('Utilisateur',related_name='owned_set', on_delete=models.CASCADE)
    matricule = models.CharField(max_length=9, null=True)
    parametres_voiture = models.ForeignKey('Parametres_voiture',related_name='related_cars', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{{\n \t car_id : {},\n \t matricule : {},\n \t date_creation : {},\n \t date_modif : {} \n}}".format(self.car_id, self.matricule, self.date_creation, self.date_modif)

class Parametres_voiture(models.Model):
    #Table qui étend la table voiture
    #parametres en flottant car on en aura besoin pour les methodes
    #numeriques qu'on va utiliser pour le calcul de la conso
    param_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_modele = models.CharField(max_length=45, null=True)
    parametre_1 = models.FloatField(default=0)
    parametre_2 = models.FloatField(default=0)


class Utilisateur_loue_voiture(models.Model):
    ulv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey('Utilisateur',related_name='cars_set', on_delete=models.CASCADE)
    voiture = models.ForeignKey('Voiture',related_name='users_set', on_delete=models.CASCADE)
    nom = models.CharField(max_length=45, null=True)
    date_transaction = models.DateTimeField(auto_now=True)
    consommation = models.FloatField(default=0)
    titre_conso =  models.CharField(max_length=45, null=True)

    def __str__(self):
        return "{{\n \t utilisateur : {!s:>},\n \t voiture_louee : {!s:>},\n \t date_transaction : {},\n \t consommation : {}\n}}".format(self.utilisateur, self.voiture, self.date_transaction, self.consommation)
