# Base imports
import os

# Django imports
from django.core.exceptions import ValidationError


def valid_extension(fieldfile_obj):
    """ Validator for txt extension. """
    ext = os.path.splitext(fieldfile_obj.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')