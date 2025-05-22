from fastapi import HTTPException, status


class BaseAuthException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "auth exception"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserExistsException(BaseAuthException):
    status_code = status.HTTP_409_CONFLICT
    detail = "user already exists"


class InvalidAuthDataException(BaseAuthException):
    detail = "invalid email or password"


class InvalidTokenException(BaseAuthException):
    detail = "Invalid token"


class TokenExpiredException(BaseAuthException):
    detail = "token expired"


class BookingException(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "no free rooms"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
