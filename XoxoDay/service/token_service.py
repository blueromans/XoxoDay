import datetime

from XoxoDay.exception import XoxoDayException
from XoxoDay.helper.token import get_token, update_token, get_cookie
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
        try:
            res = self.connect('POST', '/v1/oauth/token/user', payloads, headers)
        except XoxoDayException as e:
            res = self.recreate_access_token(payloads, headers)
        update_token(res)
        return res

    def recreate_access_token(self, payloads, headers):
        payload = {"query": "oauth_plum.query.getOauthToken", "tag": "oauth_plum",
                   "variables": {"scope": "plum_pro_api", "client_id": payloads['client_id']}}
        headers['Referer'] = "https://stagingstores.xoxoday.com/admin/accounts/platform-preferences"
        headers['pltfm'] = '4'
        headers['Cookie'] = get_cookie()
        res = self.connect('POST', 'https://stagingstores.xoxoday.com/chef/api/graph/oauth_plum/getOauthToken', payload,
                           headers, is_direct=True)
        data = res['data']['getOauthToken']
        result = {
            "access_token": data['access_token'],
            "token_type": data['token_type'],
            "expires_in": data['expires_in'],
            "refresh_token": data['refresh_token']
        }
        update_token(result)
        return result

    def create_access_token(self, payloads, headers):
        res = self.connect('POST', '/v1/oauth/token/user', payloads, headers)
        if 'error' in res:
            raise XoxoDayException(res['error'] + ' ' + res['error_description'])
        update_token(res)
        return res

    def validate_access_token(self, payloads, headers):
        try:
            res = self.connect('GET', '/v1/oauth/token', headers=headers)
        except XoxoDayException as e:
            res = self.recreate_access_token(payloads, headers)
        update_token(res)
        return res
