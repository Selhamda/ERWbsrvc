from django.urls import include, re_path
from .views import *

urlpatterns = [
        re_path(r'^voitures/$',VoitureCreateView.as_view(),name='creer_voiture'),
        re_path(r'^utilisateurs/$',UtilisateurCreateView.as_view(),name='creer_utilisateur'),
        re_path(r'^ulv/$',ULVCreateView.as_view(),name='creer_ulv'),
        re_path(r'^(?P<matricule>([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1})/details/$',FullVoitureRetrieveView.as_view(), name='details_voiture'),
        re_path(r'^(?P<matricule>([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1})/parametres/$',ParametresRetriveView.as_view(), name='param_voiture'),
        re_path(r'^(?P<matricule>([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1})/consommation/$',ConsoVoitureRetrieveView.as_view(), name='consommation'),
        re_path(r'^(?P<matricule>([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1})/updestroy/$',FullVoitureUDView.as_view(), name='updestroy'),
        re_path(r'^(?P<user_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/compte/$',UtilisateurRUDView.as_view(), name='compte'),
        re_path(r'ulvdestroy/(?P<ulv_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',ULVDestroyView.as_view(),name='destroy_ulv'),
        re_path(r'^retrieve/$',OTPCreationView.as_view(), name='creer_otp'),
        re_path(r'^verify/$',OTPVerifyView.as_view(), name='verifier_otp'),
    ]
