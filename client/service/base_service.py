import json
import requests

from typing import Dict, Tuple, Any
from client.exception.api_call_exception import ApiCallException
from client.exception.unauthenticated_exception import UnauthenticatedException
from ..config import Config

class BaseService:

    def __init__(self, config: Config, headers: Dict) -> None:
        self.config = config
        self.base_url = f'{config.API_HOST}:{config.API_PORT}/{config.API_PREFIX}'
        self.headers = {}
        for key in headers:
            self.headers[key] = headers[key]


    def fetch_request_url(self, resource_url: str) -> str:
        return f'{self.base_url}/{resource_url}'


    def fetch_request_headers(self, headers: Dict = {'Content-Type': 'application/json'}) -> Dict:
        request_headers = {}
        for key in self.headers:
            request_headers[key] = self.headers[key]
        for key in headers:
            request_headers[key] = headers[key]
        return request_headers


    def set_headers(self, headers: Dict = {}) -> None:
        for key in headers:
            self.headers[key] = headers[key]


    def print_request_debug_log_messages(self, resource_url: str, headers: Dict = {}, params: Dict = {}, payload: Dict = {}) -> None:
        request_url = self.fetch_request_url(resource_url)
        print(
            f'''
                -------- Http Request --------
                {self.__class__.__name__}: (
                    request_url: {request_url},
                    headers: {headers},
                    params: {params},
                    payload: {payload},
                )
                -------- Http Request --------
            '''
        )


    def print_response_debug_log_messages(self, resource_url: str, response: Any) -> None:
        request_url = self.fetch_request_url(resource_url)
        print(
            f'''
                -------- Http Response --------
                {self.__class__.__name__}: (
                    request_url: {request_url},
                    status_code: {response.status_code},
                    payload: {response.text},
                )
                -------- Http Response --------
            '''
        )


    def handle_response(self, response: Any) -> None:
        status_code = response.status_code

        if status_code == 403:
            raise UnauthenticatedException()
        elif status_code < 200 or status_code >= 300:
            raise ApiCallException(response.text)

    def get(self, resource_url: str, headers: Dict = {}, params: Dict = {}) -> Tuple[int, Any]:
        request_headers = self.fetch_request_headers(headers)
        request_url = self.fetch_request_url(resource_url)

        self.print_request_debug_log_messages(
            resource_url,
            headers=request_headers,
            params=params,
        )
        try:
            response = requests.get(
                request_url,
                params=params,
                headers=request_headers,
            )
            self.print_response_debug_log_messages(
                resource_url,
                response,
            )
            self.handle_response(response)
            return response.status_code, response.json()
        except Exception as e:
            raise e


    def post(self, resource_url: str, payload: Dict = {}) -> Tuple[int, Dict]:
        request_headers = self.fetch_request_headers()
        request_url = self.fetch_request_url(resource_url)

        self.print_request_debug_log_messages(
            resource_url,
            headers=request_headers,
            payload=payload,
        )
        try:
            response = requests.post(
                request_url,
                data=json.dumps(payload) if payload != False else payload,
                headers=request_headers,
            )
            self.print_response_debug_log_messages(
                resource_url,
                response,
            )
            self.handle_response(response)
            return response.status_code, response.json()
        except Exception as e:
            raise e


    def put(self, resource_url: str, payload: Dict = {}) -> Tuple[int, Dict]:
        pass


    def delete(self, resource_url: str, payload: Dict = {}) -> Tuple[int, Dict]:
        pass


    def __repr__(self):
        return f'''
            {self.__class__.__name__}: (
                base_url: {self.base_url},
                headers: {self.headers},
            )
        '''

