from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Utilisateur, Voiture, Parametres_voiture, Utilisateur_loue_voiture
from .serializers import FullUtilisateurSerializer, BasicVoitureSerializer, ULVSerializer
from random import random,randint
from decimal import Decimal
from django.core import mail
# Create your tests here.



#######Test cases for models
#####
###

class  UtilisateurTestCase(TestCase):

    def setUp(self):
        self.testusr = Utilisateur(email="user@test.com")

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
        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.parametres = Parametres_voiture.objects.create(nom_modele='testmodel')
        self.testvoiture = Voiture(parametres_voiture=self.parametres, proprietaire=self.owner, matricule=str(randint(100,999))+'-AA-'+str(randint(10,99)))

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
        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.testparam = Parametres_voiture(nom_modele='testmodel')

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
        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.parametres = Parametres_voiture.objects.create(nom_modele='testmodel')
        self.testvoiture = Voiture(parametres_voiture=self.parametres, proprietaire=self.owner, matricule=str(randint(100,999))+'-AA-'+str(randint(10,99)))
        self.testvoiture.save()
        self.testusr = Utilisateur(email="user@test.com")
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
        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.parametres = []
        self.cars = []
        self.ulvs = []
        self.reponses = []
        self.reponses2 = []

        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(email="user"+str(i)+"@test.com"))

        for i in range(3):
            self.parametres.append(Parametres_voiture.objects.create(nom_modele='testmodel'+str(i),parametre_1=40*random(),parametre_2=120*random()))

        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(parametres_voiture=self.parametres[i%3], proprietaire=self.owner, matricule=str(randint(100,999))+'-AA-'+str(randint(10,99))))


        for i in range(self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[0],
                consommation = 100**random(),
                nom = 'voit_user'+str(i+1),
                ))
        for i in range(1,self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[1],
                consommation = 10,
                nom = 'voit_user'+str(i+1),
                ))
        for i in range(1,self.nb_users):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.users[i],
                voiture = self.cars[1],
                consommation = 15,
                nom = 'voit_user'+str(i+1),
                ))
        for i in range(2):
            self.ulvs.append(Utilisateur_loue_voiture.objects.create(
                utilisateur = self.owner,
                voiture = self.cars[i],
                nom = 'testowner',
                ))
        for car in self.cars:
            self.reponses.append(self.client.get(
                reverse('details_voiture',
                kwargs={'matricule': car.matricule}),
                format="json"
            ))

        #setup for consommation
        for car in self.cars:
            self.reponses2.append(self.client.get(
                reverse('consommation',
                kwargs={'matricule': car.matricule}),
                format="json"
            ))

        #setup for create test
        mat = str(randint(100,999))+'-AA-'+str(randint(10,99))
        self.voiture_data = {
            'parametres_voiture' : 'testmodel1',
            'matricule': mat,
            'proprietaire': FullUtilisateurSerializer(instance=self.owner).data.get('user_id'),
            'nom_proprietaire': 'testowner'
        }
        self.reponse = self.client.post(
            reverse('creer_voiture'),
            self.voiture_data,
            format="json"
        )

        #setup for update test
        self.new_voiture_data = {
            'proprietaire' : FullUtilisateurSerializer(instance=self.owner).data.get('user_id'),
            'parametres_voiture' : 'testmodel0',
            'nom_proprietaire': 'testowner1',
        }
        self.reponses.append(self.client.put(
            reverse('updestroy',
            kwargs ={'matricule': mat}),
            self.new_voiture_data,
            format="json"
            ))

        #setup for delete test
        self.nb = Voiture.objects.count()
        self.reponses.append(self.client.delete(
            reverse(
                'updestroy',
                kwargs = {'matricule': mat,},
            ),
            format = "json"
        ))

        #setup for list test
        self.reponses.append(self.client.get(
            reverse('param_voiture'),
            format='json'
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

    def test_serializer_can_retrieve_consommation(self):
        #test si on peut afficher la conso de la voiture
        for i in range(self.nb_cars):

            #print(self.reponses2[i].content)
            self.assertEqual(self.reponses2[i].status_code, status.HTTP_200_OK)

    def test_serializer_can_update(self):
        #test si on eut maj les infos de la voiture
        #print(self.reponse.content)
        #print(self.reponses[self.nb_cars].content)
        self.assertEqual(self.reponses[self.nb_cars].status_code, status.HTTP_200_OK)

    def test_serializer_can_destroy(self):
        new_nb = Voiture.objects.count()
        #test si une voiture a bien ete surpprimee
        self.assertTrue(new_nb<self.nb)

    def test_parametres_can_list(self):
        print(self.reponses[self.nb_cars+2].content)
        self.assertEqual(self.reponses[self.nb_cars+2].status_code, status.HTTP_200_OK)

class UtilisateurSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        #setup for retrieve test

        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.cars = []
        self.ulvs = []
        self.parametres = []
        self.reponses = []

        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(email="user"+str(i)+"@test.com"))

        for i in range(3):
            self.parametres.append(Parametres_voiture.objects.create(nom_modele='testmodel'+str(i),parametre_1=40*random(),parametre_2=120*random()))

        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(parametres_voiture=self.parametres[i%3], proprietaire=self.owner, matricule=str(randint(100,999))+'-AA-'+str(randint(10,99))))

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
                reverse('compte',
                kwargs={'user_id': user.user_id}),
                format="json"
            ))
        #setup for create test
        self.reponse = self.client.post(
            reverse('creer_utilisateur'),
            {'email':'user@createtest.com'},
            format="json"
        )

        #setup for update test
        uid = self.reponse.data['user_id']
        self.reponses.append(self.client.put(
            reverse('compte',
            kwargs = {'user_id':uid}
            ),
        format = "json"
        ))

        #setup for delete test
        self.nb = Utilisateur.objects.count()
        self.reponses.append(self.client.delete(
            reverse('compte',
            kwargs = {'user_id':uid}),
            format = "json"
        ))


    def test_serializer_can_create(self):
        #test si on peut creer une instance du modele

        #print(self.reponse.content)
        self.assertEqual(self.reponse.status_code, status.HTTP_201_CREATED)

    def test_serializer_can_retrieve_cars(self):
        #test si on peut recup une instance
        for i in range(self.nb_users):
            #print(self.reponses[i].content)
            self.assertEqual(self.reponses[i].status_code, status.HTTP_200_OK)

    def test_serializer_can_update(self):
        #test si on peut maj une instance
        #print(self.reponses[self.nb_users].content)
        self.assertEqual(self.reponses[self.nb_users].status_code, status.HTTP_200_OK)

    def test_serializer_can_destroy(self):
        #test si on peut suppr un tuilisateur
        new_nb = Utilisateur.objects.count()
        self.assertTrue(new_nb<self.nb)


class ULVSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        #steup for creation test
        self.owner = Utilisateur(email="owner@owner.com")
        self.owner.save()
        self.nb_cars = 2
        self.nb_users = 3
        self.users = []
        self.cars = []
        self.ulv_data = []
        self.parametres = []
        self.reponses = []

        for i in range(self.nb_users):
            self.users.append(Utilisateur.objects.create(email="user"+str(i)+"@test.com"))

        for i in range(3):
            self.parametres.append(Parametres_voiture.objects.create(nom_modele='testmodel'+str(i),parametre_1=40*random(),parametre_2=120*random()))

        for i in range(self.nb_cars):
            self.cars.append(Voiture.objects.create(parametres_voiture=self.parametres[i%3], proprietaire=self.owner, matricule=str(randint(100,999))+'-AA-'+str(randint(10,99))))


        for i in range(self.nb_users):
            self.ulv_data.append({
                'utilisateur': FullUtilisateurSerializer(instance=self.users[i]).data.get('user_id'),
                'voiture' : BasicVoitureSerializer(instance=self.cars[0]).data.get('matricule'),
                'consommation' : 100*random(),
                'nom': 'ulv_user'+str(i+1),
                })
        for i in range(1,self.nb_users):
            self.ulv_data.append({
                'utilisateur': FullUtilisateurSerializer(instance=self.users[i]).data.get('user_id'),
                'voiture' : BasicVoitureSerializer(instance=self.cars[1]).data.get('matricule'),
                'consommation' : 100**random() ,
                'nom': 'ulv_user'+str(i+1),
                })

        for i in range(2*self.nb_users-1):
            self.reponses.append(self.client.post(
                reverse('creer_ulv'),
                self.ulv_data[i],
                format="json"
            ))

        #for unique testing
        #2 users with same name
        self.ulv_data.append({
            'utilisateur': FullUtilisateurSerializer(instance=self.users[1]).data.get('user_id'),
            'voiture' : BasicVoitureSerializer(instance=self.cars[1]).data.get('matricule'),
            'consommation' : float('nan') ,
            'nom': 'ulv_user'+str(3),
        })
        self.reponses.append(self.client.post(
            reverse('creer_ulv'),
            self.ulv_data[2*self.nb_users-1],
            format="json"
        ))
        #1 user with 2 names
        self.ulv_data.append({
            'utilisateur': FullUtilisateurSerializer(instance=self.users[0]).data.get('user_id'),
            'voiture' : BasicVoitureSerializer(instance=self.cars[1]).data.get('matricule'),
            'consommation' : float('inf') ,
            'nom': 'ulv_user'+str(2),
        })
        self.reponses.append(self.client.post(
            reverse('creer_ulv'),
            self.ulv_data[2*self.nb_users],
            format="json"
        ))


        #setup for delete test
        self.nb_ulv = Utilisateur_loue_voiture.objects.count()
        self.destroy_ulv_data = {
            'ulv_id': self.reponses[1].data['ulv_id'],
        }
        self.reponses.append(self.client.delete(
            reverse('destroy_ulv',
            kwargs = {**self.destroy_ulv_data,}),
            format = "json"
        ))

    def test_serializer_can_create(self):
        for i in range(self.nb_cars + self.nb_users):
            #test si on peut creer une instance du modele
            #print(self.reponses[i].content)
            self.assertEqual(self.reponses[i].status_code, status.HTTP_201_CREATED)

    def test_serializer_can_destroy(self):
        new_nb_ulv = Utilisateur_loue_voiture.objects.count()
        self.assertTrue(new_nb_ulv<self.nb_ulv)

    def test_unique_validation(self):
        #print(self.reponses[2*self.nb_users-1].content)
        #print(self.reponses[2*self.nb_users].content)
        self.assertEqual(self.reponses[2*self.nb_users-1].status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.reponses[2*self.nb_users].status_code, status.HTTP_400_BAD_REQUEST)

class OTPSerializerTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Utilisateur.objects.create(email="user@test.com")
        self.data = []
        self.reponses = []

        #for otp create test
        user_email = self.user.email
        self.data.append({
            'email': user_email,
        })
        self.reponses.append(self.client.post(
            reverse('creer_otp'),
            self.data[0],
            format="json"
        ))
        """
        #for otp verify test
        self.data.append({
            'otp' : self.reponses[0].data['otp'],
            'email': user_email,
        })
        self.reponses.append(self.client.post(
            reverse('verifier_otp'),
            self.data[1],
            format="json"
        ))"""

    def test_api_can_create_otp(self):
        #print(self.reponses[0].content)
        #print(mail.outbox[0].body)
        self.assertEqual(self.reponses[0].status_code, status.HTTP_200_OK)
"""
    def test_api_can_verify_otp(self):
        #print(self.reponses[1].content)
        self.assertEqual(self.reponses[0].status_code, status.HTTP_200_OK)"""
