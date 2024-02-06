from fastapi import HTTPException, status


class EcommerceException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


def raise_http_exception(exception_class):
    raise HTTPException(
        status_code=exception_class.status_code, detail=exception_class.detail
    )


class ForbiddenException(EcommerceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden"


class ReferralCodeNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Referral Code Not Found."


class ReferralNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Referrals Not Found."


class ReferrerNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Referrer Not Found."


class EmailNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Email Not Found."


class UserIsAlreadyReferral(EcommerceException):
    status_code = status.HTTP_409_CONFLICT
    detail = "You are already a Referral of this Referrer."


class WrongNameOrSurnameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid First Name or Last Name."


class InvalidEmailException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Please Enter a valid Email."


class ReferralCodeNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed To Add Referral Code."
