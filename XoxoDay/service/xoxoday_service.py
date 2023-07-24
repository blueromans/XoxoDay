import json
import os
import uuid
from XoxoDay.exception import ErrorCodes, XoxoDayException
from XoxoDay.service.token_service import TokenService


class XoxoDayService(TokenService):
    params = dict()
    API_DEV_URL = 'https://stagingaccount.xoxoday.com/chef'
    API_PROD_URL = 'https://accounts.xoxoday.com/chef'

    def __init__(self, **kwargs):
        self.environment = os.environ.get('XOXODAY_ENV', kwargs.get('environment', 'dev'))
        if self.environment is None:
            raise ValueError(ErrorCodes.ENVIRONMENT_ERROR)
        self.access_token = os.environ.get('XOXODAY_ACCESS_TOKEN', kwargs.get('access_token', None))
        if self.access_token is None:
            raise ValueError(ErrorCodes.ACCESS_TOKEN_ERROR)
        self.refresh_token = os.environ.get('XOXODAY_REFRESH_TOKEN', kwargs.get('refresh_token', None))
        if self.refresh_token is None:
            raise ValueError(ErrorCodes.REFRESH_TOKEN_ERROR)
        self.client_id = os.environ.get('XOXODAY_CLIENT_ID', kwargs.get('client_id', None))
        if self.client_id is None:
            raise ValueError(ErrorCodes.CLIENT_ID_ERROR)
        self.client_secret = os.environ.get('XOXODAY_CLIENT_SECRET', kwargs.get('client_secret', None))
        if self.client_secret is None:
            raise ValueError(ErrorCodes.CLIENT_SECRET_ERROR)
        api_url = self.API_DEV_URL if self.environment == 'dev' else self.API_PROD_URL
        payload = {
            "grant_type": kwargs.get('grant_type', 'refresh_token'),
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        super().__init__(api_url, self.access_token, **payload)
        token = self.token_dict['access_token']
        self.headers = {
            'Authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    @staticmethod
    def handleVoucher(item):
        return dict(id=item['productId'], name=item['name'], denominations=item['valueDenominations'])

    @staticmethod
    def handleOrder(item):
        return dict(id=item['orderId'], link=item['vouchers'][0]['voucherCode'], poNumber=item['poNumber'])

    def handleVouchers(self, items):
        return list(map(lambda item: self.handleVoucher(item), items['data']['getVouchers']['data']))

    def getVouchers(self, filters=None, includeProducts=None):
        payload_file_path = f'{os.path.dirname(os.path.abspath(__file__))}/voucher.json'
        file = open(payload_file_path)
        payload = json.load(file)
        if filters is not None:
            responses = []
            for filter_el in filters:
                payload['variables']['data']['filters'] = [filter_el]
                response = self.connect('POST', '/v1/oauth/api', payload, headers=self.headers)
                response = self.handleVouchers(response)
                responses = responses + response
            return responses
        if includeProducts is not None:
            payload['variables']['data']['includeProducts'] = includeProducts
            response = self.connect('POST', '/v1/oauth/api', payload, headers=self.headers)
            return self.handleVouchers(response)
        response = self.connect('POST', '/v1/oauth/api', payload, headers=self.headers)
        response = self.handleVouchers(response)
        return response

    def placeOrder(self, email, productId, denomination, poNumber=None):
        payload_file_path = f'{os.path.dirname(os.path.abspath(__file__))}/placeOrder.json'
        file = open(payload_file_path)
        payload = json.load(file)
        product = self.getVouchers(includeProducts=productId)
        if len(product) == 0:
            raise XoxoDayException(ErrorCodes.INVALID_ATTRIBUTE)
        if poNumber is None:
            poNumber = str(uuid.uuid4())
        payload['variables']['data']['productId'] = productId
        payload['variables']['data']['denomination'] = denomination
        payload['variables']['data']['email'] = email
        payload['variables']['data']['poNumber'] = poNumber
        response = self.connect('POST', '/v1/oauth/api', payload, headers=self.headers)
        response['data']['placeOrder']['data']['poNumber'] = poNumber
        return self.handleOrder(response['data']['placeOrder']['data'])
