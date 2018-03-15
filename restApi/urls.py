from django.urls import include, re_path
from .views import VoitureCreateView,VoitureRetrieveUpdateView,UtilisateurCreateView,ULVCreateView, UtilisateurRetrieveUpdateView, ULVRetrieveUpdateView

urlpatterns = [
        re_path(r'^voitures/$',VoitureCreateView.as_view(),name='creer_voiture'),
        re_path(r'^utilisateurs/$',UtilisateurCreateView.as_view(),name='creer_utilisateur'),
        re_path(r'^ulv/$',ULVCreateView.as_view(),name='creer_ulv'),
        re_path(r'^voitures/(?P<car_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',VoitureRetrieveUpdateView.as_view(), name='details_voiture'),
        re_path(r'^utilisateurs/(?P<user_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',UtilisateurRetrieveUpdateView.as_view(), name='details_utilisateur'),
        re_path(r'ulvs/(?P<utilisateur>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/(?P<voiture>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',ULVRetrieveUpdateView.as_view(),name='details_ulv'),
    ]