from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
import re
import math

def matricule_syntax(value):
    pattern = re.compile("([A-Z]{2}-[0-9]{3}-[A-Z]{2}){1}|([0-9]{3}-[A-Z]{2}-[0-9]{2}){1}")
    if pattern.search(value) == None:
        raise ValidationError({
            'Field syntax is invalid'
            })

class ConsoFloatValidator(object):

    message = _('NaN, infinity and -infinity are not JSON compliant')

    def __init__(self, field, message=None):
        self.field = field
        self.message = message or self.message

    def __call__(self, value):
        if math.isinf(value):
            raise ValidationError({
                self.field : self.message
            })
        if math.isnan(value):
            raise ValidationError({
                self.field : self.message
            })
