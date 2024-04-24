from django.core.exceptions import ValidationError
from rest_framework import status


class UnavailableTimeSpansError(ValidationError):
    message = "unavailable"
    status_code = status.HTTP_200_OK

    def __init__(
        self,
        message=None,
        code=None,
        params={},
    ):
        super().__init__(
            message=self.message,
            params=params,
            code=code,
        )
