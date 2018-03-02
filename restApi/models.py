from django.db import models

# Create your models here.

class Utilisateur(models.Model):
    prenom = models.CharField(max_length=45, blank=True, null=True)
    nom = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    depenses_utilisateur = models.OneToOneField('Depenses_utilisateur',on_delete=models.CASCADE)

    def __str__(self):
        return "id:{}\n {}{}, ajouté le {}".format(self.id, self.prenom,self.nom, self.date_creation)

class Depenses_utilisateur(models.Model):
    #J'utilise une representation decimale ici pour l'ergonomie, c plus lisible pour l'utilisateur
    depenses_util = models.DecimalField(max_digits=6,decimal_places=2)
    date_depense = models.DateTimeField(auto_now_add=True)
    voiture_utilisee = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return "Le {} vous avez depensé {} en conduisant la voiture {}".format(self.date_depense, self.depenses_util, self.voiture_utilisee)

class Voiture(models.Model):
    nom_modele = models.CharField(max_length=45, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True) 
    parametres_voiture = models.OneToOneField('Parametres_voiture',on_delete=models.CASCADE)   

    def __str__(self):
        return "id:{}\n {}, ajoutée le {}".format(self.id, self.nom_modele, self.date_creation)

class Parametres_voiture(models.Model):
    #parametres en flottant car on en a besoin pour les methodes
    #numeriques qu'on va utiliser pour le calcul de la conso
    parametre_1 = models.FloatField()
    date_modif = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "parametre_1 = {}, derniere modification le {}".format(self.parametres, self.date_modif)

class Utilisateur_loue_voiture(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    voiture = models.ForeignKey('Voiture', on_delete=models.CASCADE)
    date_debut_location = models.DateTimeField(auto_now_add=True)
    date_fin_location = models.DateTimeField(auto_now=True)
    #DecimaField encore une fois pour l'ergonomie
    consommation_instantanee = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return "utilisateur {} loue voiture {} depuis {} jusqu'à {} et a consommé {}".format(self.utilisateur, self.voiture, self.date_debut_location, self.date_fin_location, self.consommation_instantanee)



