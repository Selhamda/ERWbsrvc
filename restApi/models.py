from django.db import models

# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "id:{},\n nom:{},\n ajouté le: {}".format(self.id, self.nom, self.date_creation)

class Voiture(models.Model):
    nom_modele = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
          

    def __str__(self):
        return "id: {},\n nom de modele: {},\n ajoutée le: {}".format(self.id, self.nom_modele, self.date_creation)

class Parametres_voiture(models.Model):
    #Table qui étend la table voiture
    #parametres en flottant car on en a besoin pour les methodes
    #numeriques qu'on va utiliser pour le calcul de la conso
    parametre_1 = models.FloatField(default=0)
    parametre_2 = models.FloatField(default=0)
    date_modif = models.DateTimeField(auto_now=True)
    voiture = models.OneToOneField('Voiture', models.SET_NULL,blank=True, null=True) 
    def __str__(self):
        return "{!s:>},\n parametre_1: {},\n parametre_2: {},\n derniere modification: {}".format(self.voiture, self.parametre_1,self.parametre_2, self.date_modif)

class Utilisateur_loue_voiture(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    voiture = models.ForeignKey('Voiture', on_delete=models.CASCADE)
    date_debut_location = models.DateTimeField(auto_now_add=True)
    date_fin_location = models.DateTimeField(auto_now=True)
    #DecimaField encore une fois pour l'ergonomie
    consommation= models.DecimalField(max_digits=6,decimal_places=2,default=0)

    def __str__(self):
        return 'utilisateur:\n {!s:>},\n voiture louee:\n {!s:>},\n depuis {},\n consommation: {}'.format(self.utilisateur, self.voiture, self.date_debut_location, self.date_fin_location, self.consommation)



