import datetime

from XoxoDay.exception import XoxoDayException
from XoxoDay.helper.token import get_token, update_token
from XoxoDay.service.http_service import HttpService


class TokenService(HttpService):
    def __init__(self, REST_URL, access_token=None, **payloads):
        if payloads is None:
            raise XoxoDayException("Payloads required!")
        super().__init__(REST_URL)
        self.payloads = payloads
        self.token_dict = get_token()
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        if self.token_dict is None:
            self.access_token = access_token
            headers['Authorization'] = f'Bearer {self.access_token}'
            self.token_dict = self.retrieve_access_token(payloads, headers)
            return
        headers['Authorization'] = f'Bearer {self.token_dict["access_token"]}'
        self.token_dict = self.validate_access_token(payloads, headers)
        if datetime.datetime.now() < datetime.datetime.now() + datetime.timedelta(
                seconds=int(self.token_dict['expires_in'])):
            return
        self.token_dict = self.retrieve_access_token(payloads, headers)

    def retrieve_access_token(self, payloads, headers):
        del headers['Authorization']
        res = self.connect('POST', '/v1/oauth/token/user', payloads, headers)
        update_token(res)
        return res

    def create_access_token(self, payloads, headers):
        res = self.connect('POST', '/v1/oauth/token/user', payloads, headers)
        if 'error' in res:
            raise XoxoDayException(res['error'] + ' ' + res['error_description'])
        update_token(res)
        return res

    def validate_access_token(self, payloads, headers):
        res = self.connect('GET', '/v1/oauth/token', headers=headers)
        update_token(res)
        return res
