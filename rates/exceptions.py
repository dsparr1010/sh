class UnavailableTimeSpansError(BaseException):
    pass


class NoInstanceFound(BaseException):
    message = "No instance found to update"


class NothingToUpdate(BaseException):
    message = "Given data matches perfectly - nothing to update"
