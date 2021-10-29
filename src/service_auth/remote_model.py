
import requests
import json
from django.conf import settings 

class RemoteModel:
    def __init__(self, request, entity, endpoint,token=None):
        self.request = request
        self.entity = entity
        self.endpoint = endpoint
        self.override_headers = {'Authorization':token}

        self.url = f'{settings.ENTITY_BASE_URL_MAP.get(entity)}/{endpoint}'

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
        data = {'token':token.split(' ')[1]}
        return requests.post(
        url,json.dumps(data),
        headers=self._headers(),
        cookies=self._cookies())

    def get(self, entity_id):
        return requests.get(
        f'{self.url}/{entity_id}',
        headers=self._headers(),
        cookies=self._cookies())
    
    def get(self):
        url = f'{self.url}/'
        return requests.get(
        url,
        headers=self._headers(),
        cookies=self._cookies())

    def delete(self, entity_id):
        return requests.delete(
        f'{self.url}/{entity_id}',
        headers=self._headers(),
        cookies=self._cookies())

    def create(self, entity_id, entity_data):
        return requests.put(
        f'{self.url}/',
        data=json.dumps(entity_data),
        headers=self._headers(),
        cookies=self._cookies())

    def update(self, entity_id, entity_data):
        return requests.post(
        f'{self.url}/{entity_id}',
        data=json.dumps(entity_data),
        headers=self._headers(),
        cookies=self._cookies())

