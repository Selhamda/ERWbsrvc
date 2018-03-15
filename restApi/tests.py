from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture
from .serializers import UtilisateurSerializer, VoitureSerializer, ULVSerializer
from random import random,randint
from decimal import Decimal
# Create your tests here.



#######Test cases for models
#####
###
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




#######Test cases for serializers
#####
###
class VoitureSerializerTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        #setup for retireve test
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.cars = []
        self.ulvs = []
        self.reponses = []
        
        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(nom = 'user'+str(i+1)))
        
        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(nom_modele='car'+str(i+1)))
        
        for car in self.cars:
            Parametres_voiture.objects.create(parametre_1=40*random(),parametre_2=120*random(),voiture=car)

        for i in range(self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[0],
                consommation = 100**random() ,
                ))
        for i in range(1,self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[1],
                consommation = 100**random() ,
                ))
        for car in self.cars:
            self.reponses.append(self.client.get(
                reverse('details_voiture',
                kwargs={'car_id': car.car_id}),
                format="json"
            ))

        #setup for create test
        self.voiture_data = {
            'nom_modele' : 'renaut 205',
            'parametres_voiture' : {'parametre_1' : 42,'parametre_2' : 777,},
        }
        self.reponse = self.client.post(
            reverse('creer_voiture'),
            self.voiture_data,
            format="json"
        )

        #setup for update test
        self.new_voiture_data = {
            'nom_modele' : 'peugeot 208',
            'parametres_voiture' : {'parametre_1': 7, 'parametre_2': 23,},
        }
        voit_id = Voiture.objects.get(nom_modele='renaut 205').car_id
        self.reponses.append(self.client.put(
            reverse('details_voiture',
            kwargs ={'car_id': voit_id}),
            self.new_voiture_data,
            format="json"
            ))

    def test_serializer_can_create(self):
        #test si on peut creer une instance du modele

        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)
    
    def test_serializer_can_retrieve_users(self):
        #test si on peut afficher les details de la voiture

        for i in range(self.nb_cars):
            #print(self.reponses[i].content)
            self.assertEqual(self.reponses[i].status_code, status.HTTP_200_OK)
    
    def test_serializer_can_update(self):
        #test si on eut maj les infos de la voiture
        #print(self.reponse.content)
        #print(self.reponses[-1].content)
        self.assertEqual(self.reponses[-1].status_code, status.HTTP_200_OK)

class UtilisateurSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        #setup for retrive test
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.cars = []
        self.ulvs = []
        self.reponses = []
        
        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(nom = 'user'+str(i+1)))
        
        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(nom_modele='car'+str(i+1)))
        
        for car in self.cars:
            Parametres_voiture.objects.create(parametre_1=40*random(),parametre_2=120*random(),voiture=car)

        for i in range(self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[0],
                consommation = 100**random() ,
                ))
        for i in range(1,self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[1],
                consommation = 100**random() ,
                ))
        for user in self.users:
            self.reponses.append(self.client.get(
                reverse('details_utilisateur',
                kwargs={'user_id': user.user_id}),
                format="json"
            ))
        #setup for create test
        self.user_data = {
            'nom' : 'Salim',
        }
        self.reponse = self.client.post(
            reverse('creer_utilisateur'),
            self.user_data,
            format="json"
        )

    def test_serializer_can_create(self):
        #test si on peut creer une instance du modele

        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)
    
    def test_serializer_can_retrieve_cars(self):        
        for i in range(self.nb_users):
            #print(self.reponses[i].content)
            self.assertEqual(self.reponses[i].status_code, status.HTTP_200_OK)        


class ULVSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        #steup for creation test
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.cars = []
        self.ulv_data= []
        self.reponses = []
        
        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(nom = 'user'+str(i+1)))
        
        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(nom_modele='car'+str(i+1)))
        
        for car in self.cars:
            Parametres_voiture.objects.create(parametre_1=40*random(),parametre_2=120*random(),voiture=car)

        for user in self.users:
            self.ulv_data.append({
                'utilisateur': UtilisateurSerializer(instance=user).data.get('user_id'),
                'voiture' : VoitureSerializer(instance=self.cars[0]).data.get('car_id'),
                'consommation' : 100*random(),
                })
        for i in range(1,self.nb_users):
            self.ulv_data.append({
                'utilisateur': UtilisateurSerializer(instance=self.users[i]).data.get('user_id'),
                'voiture' : VoitureSerializer(instance=self.cars[1]).data.get('car_id'),
                'consommation' : 100**random() ,
                })
        for i in range(5):
            self.reponses.append(self.client.post(
                reverse('creer_ulv'),
                self.ulv_data[i],
                format="json"
            ))
        
        #setup for update test
        #use patch for update here cuz partial update
        self.new_ulv_data = {
            'utilisateur': self.users[0].user_id,
            'voiture' : self.cars[0].car_id,
            'consommation' : 200,}
        self.reponses.append(self.client.put(
            reverse('details_ulv',
            kwargs = {
                'utilisateur': self.new_ulv_data.get('utilisateur'),
                'voiture' : self.new_ulv_data.get('voiture'),
                }
            ),
            self.new_ulv_data,
            format="json"
        ))

    def test_serializer_can_create(self):
        for i in range(5):
            #test si on peut creer une instance du modele

            #print(self.reponses[i].content)
            self.assertEqual(self.reponses[i].status_code, status.HTTP_201_CREATED)
    
    def test_serializer_can_update(self):
        #test si on peut maj une carte conso

        #print(self.reponses[-1].content)
        self.assertEqual(self.reponses[-1].status_code,status.HTTP_200_OK)

    
        

