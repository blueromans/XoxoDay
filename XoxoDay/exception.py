class ErrorCodes:
    INVALID_ATTRIBUTE = 'Invalid attribute!'
    INVALID_DENOMINATION = 'Invalid denomination!'
    INVALID_VOUCHER_ID = 'Invalid voucher id!'
    ENVIRONMENT_ERROR = 'Invalid environment!'
    CLIENT_ID_ERROR = 'Invalid client id!'
    CLIENT_SECRET_ERROR = 'Invalid client secret!'
    ACCESS_TOKEN_ERROR = 'Invalid access token!'
    REFRESH_TOKEN_ERROR = 'Invalid refresh token!'
    BASE_URL_ERROR = 'Invalid base url!'


class XoxoDayException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
