from django.urls import include, re_path
from .views import *

urlpatterns = [
        re_path(r'^voitures/$',VoitureCreateView.as_view(),name='creer_voiture'),
        re_path(r'^utilisateurs/$',UtilisateurCreateView.as_view(),name='creer_utilisateur'),
        re_path(r'ulv/$',ULVCreateView.as_view(),name='creer_ulv'),
    ]