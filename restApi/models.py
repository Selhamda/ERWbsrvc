from django.db import models
import uuid

# Create your models here.

class Utilisateur(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{{\n \t user_id : {},\n \t ajouté le : {}\n}}".format(self.user_id, self.date_creation)

class Voiture(models.Model):
    car_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietaire = models.ForeignKey('Utilisateur',related_name='owned_set', on_delete=models.CASCADE)
    matricule = models.CharField(max_length=9, blank=True, null=True)
    nom_modele = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{{\n \t car_id : {},\n \t nom_modele : {},\n \t date_creation : {},\n \t date_modif : {} \n}}".format(self.car_id, self.nom_modele, self.date_creation, self.date_modif)

class Parametres_voiture(models.Model):
    #Table qui étend la table voiture
    #parametres en flottant car on en aura besoin pour les methodes
    #numeriques qu'on va utiliser pour le calcul de la conso
    parametre_1 = models.FloatField(default=0)
    parametre_2 = models.FloatField(default=0)
    date_modif = models.DateTimeField(auto_now=True)
    voiture = models.OneToOneField('Voiture', models.CASCADE, null=True)
    def __str__(self):
        return " {!s:>},{{\n \t parametre_1 : {},\n \t parametre_2 : {},\n \t date_modif : {} \n}}".format(self.voiture, self.parametre_1,self.parametre_2, self.date_modif)

class Utilisateur_loue_voiture(models.Model):
    ulv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey('Utilisateur',related_name='cars_set', on_delete=models.CASCADE)
    voiture = models.ForeignKey('Voiture',related_name='users_set', on_delete=models.CASCADE)
    nom = models.CharField(max_length=45, null=True)
    date_transaction = models.DateTimeField(auto_now=True)
    consommation = models.FloatField(default=0)

    def __str__(self):
        return "{{\n \t utilisateur : {!s:>},\n \t voiture_louee : {!s:>},\n \t date_transaction : {},\n \t consommation : {}\n}}".format(self.utilisateur, self.voiture, self.date_transaction, self.consommation)
