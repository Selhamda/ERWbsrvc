from django.db import models
import uuid

# Create your models here.

class Utilisateur(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "id:{},\n nom:{},\n ajouté le: {}".format(self.user_id, self.nom, self.date_creation)

class Voiture(models.Model):
    car_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietaire = models.ForeignKey('Utilisateur',related_name='owned_set', on_delete=models.CASCADE)
    matricule = models.CharField(max_length=7, blank=True, null=True)
    nom_modele = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
          
    def __str__(self):
        return "id: {},\n nom de modele: {},\n ajoutée le: {}".format(self.car_id, self.nom_modele, self.date_creation)

class Parametres_voiture(models.Model):
    #Table qui étend la table voiture
    #parametres en flottant car on en aura besoin pour les methodes
    #numeriques qu'on va utiliser pour le calcul de la conso
    parametre_1 = models.FloatField(default=0)
    parametre_2 = models.FloatField(default=0)
    date_modif = models.DateTimeField(auto_now=True)
    voiture = models.OneToOneField('Voiture', models.CASCADE, null=True) 
    def __str__(self):
        return "{!s:>},\n parametre_1: {},\n parametre_2: {},\n derniere modification: {}".format(self.voiture, self.parametre_1,self.parametre_2, self.date_modif)

class Utilisateur_loue_voiture(models.Model):
    utilisateur = models.ForeignKey('Utilisateur',related_name='cars_set', on_delete=models.CASCADE)
    voiture = models.ForeignKey('Voiture',related_name='users_set', on_delete=models.CASCADE)
    date_transaction = models.DateTimeField(auto_now=True)
    consommation = models.FloatField(default=0)

    class Meta:
        unique_together = ('utilisateur','voiture')

    def __str__(self):
        return 'utilisateur:\n {!s:>},\n voiture louee:\n {!s:>},\n depuis {},\n consommation: {}'.format(self.utilisateur, self.voiture, self.date_transaction, self.consommation)



