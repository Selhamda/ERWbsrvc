from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
import re
import math

####Pour valider que la syntaxe du matricule envoye dans le json est valide
def matricule_syntax(value):
    pattern = re.compile("([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1}")
    if pattern.search(value) == None:
        raise ValidationError({
            'Field syntax is invalid'
            })

###Pour valider que l'email  rentre est de syntaxe correcte
"""
def email_syntax(value):
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if pattern.search(value) == None:
        raise ValidationError({
            'Email syntax is invalid'
            })
"""
class ConsoFloatValidator(object):
    ###Pour verifier qu'il n'ya pas eu d'erreur de calcull niveau algorithme et que
    ###la bdd ne contient que des flottants valides
    message = _('NaN, infinity and -infinity are not JSON compliant')

    def __init__(self, field, message=None):
        self.field = field
        self.message = message or self.message

    def __call__(self, value):
        if math.isinf(value):
            ##si la valeur retournee est infinie
            raise ValidationError({
                self.field : self.message
            })
        if math.isnan(value):
            ##si la valeur n'est pas un nombre
            raise ValidationError({
                self.field : self.message
            })
