from django.urls import include, re_path
from .views import VoitureCreateView,VoitureRUDView,UtilisateurCreateView,ULVCreateView, UtilisateurRUDView, ULVRUDView

urlpatterns = [
        re_path(r'^voitures/$',VoitureCreateView.as_view(),name='creer_voiture'),
        re_path(r'^utilisateurs/$',UtilisateurCreateView.as_view(),name='creer_utilisateur'),
        re_path(r'^ulv/$',ULVCreateView.as_view(),name='creer_ulv'),
        re_path(r'^voitures/(?P<car_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',VoitureRUDView.as_view(), name='details_voiture'),
        re_path(r'^utilisateurs/(?P<user_id>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',UtilisateurRUDView.as_view(), name='details_utilisateur'),
        re_path(r'ulvs/(?P<utilisateur>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/(?P<voiture>([a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}){1})/$',ULVRUDView.as_view(),name='details_ulv'),
    ]