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


class WrongNameOrSurnameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid First Name or Last Name."
