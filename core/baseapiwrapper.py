import requests
import xmltodict
from urllib.parse import urljoin

from core.token import get_token
from .models import APIResponse
from common.error_codes import error_codes_to_messages


class BaseAPIWrapper:
    def __init__(self):
        self.__base_url = "http://sandbox.namesilo.com/api/"
        self.token = get_token()

    def __is_response_valid(self, content):
        valid = True
        error_message = ""
        payload = content["namesilo"]["reply"]

        code = int(payload.get("code", None))

        if code != 300:
            valid = False
            error_message = error_codes_to_messages[code]

        return valid, error_message

    def get(self, url):
        api_response = APIResponse()

        try:
            api_request = requests.get(urljoin(self.__base_url, url))

            api_response.status_code = api_request.status_code
            api_response.content = api_request.content

            if api_request.status_code not in [200, 201, 202]:
                api_response.error = "API responded with status code: %s" % api_response.status_code

            api_response.content = xmltodict.parse(api_request.content.decode())

            response_valid, error_message = self.__is_response_valid(api_response.content)
            if response_valid:
                api_response.success = True
            else:
                api_response.success = False
                api_response.error = error_message

        except Exception as ex:
            api_response.success = False
            api_response.error = str(ex)

        finally:
            return api_response
