from http.client import responses
from .error_msgs import CountryCount
import json
from urllib import request
from urllib.parse import quote
import requests

class InfoPage():

    def __init__(self, url):
        self.url = url

    def make_a_request(self):
        res = request.urlopen(self.url)
        return json.loads(res.read().decode('utf-8'))

    def get_value_by_key(self, body, key):
        return body[key]

    def get_response_code(self, url):
        return requests.get(url).status_code

    def is_response_OK(self, url):
        statusCode = self.get_response_code(url)
        if (statusCode >= 400):
            return False
        return True

    def response_code_should_be_success(self):
        assert self.is_response_OK(self.url), self.responseCodeErrorMsg(self.url)

    def items_list_shouldnt_be_empty(self, items):
        assert len(items) > 0, "Items list shouldn't be empty"

    def items_list_should_be_empty(self, items, name):
        assert len(items) == 0, f"Items list should be empty, there is no city with name {name}"

    def there_is_error(self, jsonBody):
        try:
            errorBody = jsonBody['error']
            return True
        except (KeyError):
            return False
    
    def responseCodeErrorMsg(self, url):
        respCode = self.get_response_code(url)
        return f'Got Server Error {respCode}' if (respCode>=500) \
                else f'Got Client Error {respCode}' if (respCode>=400) else ''

    def there_items_on_the_page(self, url):
        self.url = url
        body = self.make_a_request()
        items = self.get_value_by_key(body,'items')
        if (len(items) > 0):
            return True
        return False 

    def get_last_page_number(self, url):
        pageNum = 1
        while (self.there_items_on_the_page(url + (str)(pageNum))):
            pageNum += 1
        self.url = url + (str)(pageNum - 1)
        return pageNum - 1

    def should_be_exact_error_msg(self, actual, expected):
        assert actual == expected, \
            f"Invalid error message, should be {expected}"
