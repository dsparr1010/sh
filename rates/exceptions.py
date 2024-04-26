from django.core.exceptions import ValidationError
from rest_framework import status


class UnavailableTimeSpansError(BaseException):
    pass
