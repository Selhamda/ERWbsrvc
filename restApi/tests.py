from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture
from .serializers import UtilisateurSerializer, VoitureSerializer
# Create your tests here.

class  UtilisateurTestCase(TestCase):

    def setUp(self):
        self.testusr = Utilisateur(nom='test user')
    
    def test_model_can_create_instance(self):
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
    
    def test_model_can_create_instance(self):
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
    
    def test_model_can_create_instance(self):
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
    
    def test_model_can_create_instance(self):
        compte = Utilisateur_loue_voiture.objects.count()
        self.ulv.save()
        new_compte = Utilisateur_loue_voiture.objects.count()
        self.assertTrue(new_compte>compte)

#    def test_model_can_print(self):
#        self.ulv.save()
#        print('/////Debut print test')
#        print(self.ulv)
#        print('/////Fin print test')
        
class VoitureSerializerTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.voiture_data = {
            'nom_modele' : 'renaut 205',
            'parametres_voiture' : {'parametre_1' : 42,'parametre_2' : 777,},
        }
        self.reponse = self.client.post(
            reverse('creer_voiture'),
            self.voiture_data,
            format="json"
        )
    
    def test_serializer_can_create(self):
        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)

class UtilisateurSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'nom' : 'Salim',
        }
        self.reponse = self.client.post(
            reverse('creer_utilisateur'),
            self.user_data,
            format="json"
        )

    def test_serializer_can_create(self):
        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)

class ULVSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = Utilisateur.objects.create(nom = 'user1')
        #self.user2 = Utilisateur.objects.create(nom = 'user2')
        #self.user3 = Utilisateur.objects.create(nom = 'user3')
        #self.user4 = Utilisateur.objects.create(nom = 'user4')
        #self.user5 = Utilisateur.objects.create(nom = 'user5')
        self.car1 = Voiture.objects.create(nom_modele='car1')
        #self.car2 = Voiture.objects.create(nom_modele='car2')
        self.param1 = Parametres_voiture.objects.create(parametre_1=42,parametre_2=42,voiture=self.car1)
        #self.param2 = Parametres_voiture.objects.create(parametre_1=77,parametre_2=77,voiture=self.car2)
        user_id = UtilisateurSerializer(instance=self.user1).data.get('user_id')
        car_id = VoitureSerializer(instance=self.car1).data.get('car_id')
        self.ulv_data = {
            'utilisateur': user_id,
            'voiture' : car_id,
            'consommation' : 50,
            }
        self.reponse = self.client.post(
            reverse('creer_ulv'),
            self.ulv_data,
            format="json"
        )
    def test_serializer_can_create(self):
        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)

