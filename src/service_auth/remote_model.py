
import requests
import json
from django.conf import settings 

class RemoteModel:
    def __init__(self, request, entity, endpoint,token = None,tenant = None):
        self.request = request
        self.entity = entity
        self.endpoint = endpoint
        self.override_headers = {'Authorization':token}
      
        self.tenant = str(str(request.tenant)+'.') if request.tenant else ''
        self.url = f'{settings.PROTOCOL}{self.tenant}{settings.ENTITY_BASE_URL_MAP.get(entity)}/{settings.ENTITY_URL_PATH.get(endpoint)}'

    def _headers(self, override_headers=None):
        base_headers = {'content-type': 'application/json'}
        override_headers = self.override_headers or {}
        return {
            # **self,
            **base_headers,
            **override_headers,
        }
        
    def _cookies(self, override_cookies=None):
        override_cookies = override_cookies or {}
        return {
        **self.request.COOKIES,
        **override_cookies,
        }

    def verify_token(self,token):
        url = f'{self.url}/'
        try:
            data = {'token':token.split(' ')[1]}
        except:
            data = {'token':token}
        return requests.post(
        url,json.dumps(data),
        headers=self._headers(),
        cookies=self._cookies())
    
    def get_permission(self,ut,perm = None):
        url = f'{self.url}/{ut}/'
        data = {'permission':perm}
        return requests.get(
        url,data,
        headers=self._headers(),
        cookies=self._cookies())

    def get_detail(self, entity_id):
        url = f'{self.url}/{entity_id}'
        return requests.get(
        url,
        headers=self._headers(),
        cookies=self._cookies())
    
    def get(self):
        url = f'{self.url}/'
        return requests.get(
        url,
        headers=self._headers(),
        cookies=self._cookies())

    def delete(self, entity_id):
        url = f'{self.url}/{entity_id}/'

        return requests.delete(
        url,
        headers=self._headers(),
        cookies=self._cookies())

    def update(self, entity_id, entity_data):
        url = f'{self.url}/{entity_id}/'
        return requests.put(
        url,
        data=json.dumps(entity_data),
        headers=self._headers(),
        cookies=self._cookies())

    def create(self, entity_data):
        url = f'{self.url}/'
        return requests.post(url,
        data=json.dumps(entity_data),
        headers=self._headers(),
        cookies=self._cookies())

