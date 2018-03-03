from rest_framework import serializers
from .models import *

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        "class meta lie les champs du serializer avec ceux du model"
        model = Utilisateur
        fields = ('id', 'nom' , 'depenses_utilisateur','date_creation', 'date_modif')
        read_only_fields = ('date_creation', 'date_modif')