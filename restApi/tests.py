from django.test import TestCase
from .models import *
from .serializers import *
# Create your tests here.

class  UtilisateurTestCase(TestCase):

    def setUp(self):
        self.testusr = Utilisateur(nom='test user')
    
    def test_creation_instance(self):
        compte = Utilisateur.objects.count()
        self.testusr.save()
        new_compte = Utilisateur.objects.count()
        self.assertTrue(new_compte>compte)

#    def test_model_can_print(self):
#        self.testusr.save()
#        print('/////Debut print test')
#        print(self.testusr)
#        print('/////Fin print test')

class  VoitureTestCase(TestCase):

    def setUp(self):
        self.testvoiture = Voiture(nom_modele='test voiture')
    
    def test_creation_instance(self):
        compte = Voiture.objects.count()
        self.testvoiture.save()
        new_compte = Voiture.objects.count()
        self.assertTrue(new_compte>compte)

#    def test_model_can_print(self):
#        self.testvoiture.save()
#        print('/////Debut print test')
#        print(self.testvoiture)
#        print('/////Fin print test')

class  Parametres_voitureTestCase(TestCase):

    def setUp(self):
        self.testvoiture = Voiture(nom_modele='test voiture')
        self.testvoiture.save()
        self.testparam = Parametres_voiture(voiture=self.testvoiture)
    
    def test_creation_instance(self):
        compte = Parametres_voiture.objects.count()
        self.testparam.save()
        new_compte = Parametres_voiture.objects.count()
        self.assertTrue(new_compte>compte)

#    def test_model_can_print(self):
#        self.testparam.save()
#        print('/////Debut print test')
#        print(self.testparam)
#        print('/////Fin print test')

class ULVTestCase(TestCase):

    def setUp(self):
        self.testvoiture = Voiture(nom_modele='test voiture')
        self.testvoiture.save()
        self.testparam = Parametres_voiture(voiture=self.testvoiture)
        self.testparam.save()
        self.testusr = Utilisateur(nom='test user')
        self.testusr.save()
        self.ulv = Utilisateur_loue_voiture(utilisateur=self.testusr,voiture=self.testvoiture)
    
    def test_creation_instance(self):
        compte = Utilisateur_loue_voiture.objects.count()
        self.ulv.save()
        new_compte = Utilisateur_loue_voiture.objects.count()
        self.assertTrue(new_compte>compte)

#    def test_model_can_print(self):
#        self.ulv.save()
#        print('/////Debut print test')
#        print(self.ulv)
#        print('/////Fin print test')
        
class ParametresVoitureSerializerTestCase(TestCase):
    pass