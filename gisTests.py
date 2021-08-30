from pages.InfoPage import InfoPage
from pages.error_msgs import CountryCount, ErrorMessages
import pytest
import time
from http.client import responses
import json
from urllib import request
from urllib.parse import quote
import requests

def test_total_count():
    url = 'https://regions-test.2gis.com/1.0/regions'
    get_request = InfoPage(url)
    get_request.response_code_should_be_success()

    body = get_request.make_a_request()
    total = get_request.get_value_by_key(body, 'total')
    assert total == 22, f"Total count must be 22, but it's {total} instead"

@pytest.mark.q_tests
class TestQParameter:

    def test_q_3_letters(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('оск')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert gotCityName == "Москва", f"Should have got 'Москва' result, but got {gotCityName} instead"

    def test_q_several_cities_count(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('рск')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"

    def test_q_capital_letter(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('Ирск')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert gotCityName == "Новосибирск", f"Should have got 'Новосибирск' result, but got {gotCityName} instead"

    def test_q_city_not_in_db(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('Вашингтон')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_should_be_empty(itemsList, 'Вашингтон')

    def test_q_caps(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('САНКТ-')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert gotCityName == "Санкт-Петербург", f"Should have got 'Санкт-Петербург' result, but got {gotCityName} instead"

    def test_q_2_letters(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + quote('ош')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, q must have at least 3 letters"
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')

        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_Q_MUST_BE_GE_THAN_3)

    def test_q_long_name(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=' + \
            quote('Крунг Тхеп Маханакхон Амон Раттанакосин Махинтараюттхая Махадилок Пхоп Ноппарат \
                Ратчатхани Буриром Удомратчанивет Махасатан Амон Пиман Аватан Сатит Саккатхаттийя Витсанукам Прасит')
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, q must have 30 letters maximum"
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')

        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_Q_MUST_BE_LE_THAN_30)

    def test_q_empty(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q='
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, q must have at least 3 letters"
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')

        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_Q_MUST_BE_GE_THAN_3)

    def test_q_exact_30_symbols(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=123456789012345678901234567890'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, "Shouldn't be an error, q must have 30 letters maximum"

    def test_q_exact_31_symbols(self):
        url = 'https://regions-test.2gis.com/1.0/regions?q=1234567890123456789012345678901'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, q must have 30 letters maximum"
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')

        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_Q_MUST_BE_LE_THAN_30)

    @pytest.mark.parametrize('page_q_params', ["q="+quote('рск')+"&page=3", "page=3&q="+quote('рск')])
    def test_q_ignore_page(self, page_q_params):
        url = 'https://regions-test.2gis.com/1.0/regions?' + page_q_params
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"

    @pytest.mark.parametrize('page_q_params', ["q="+quote('рск')+"&page=0", "page=0&q="+quote('рск')])
    def test_q_ignore_incorrect_page(self, page_q_params):
        url = 'https://regions-test.2gis.com/1.0/regions?' + page_q_params
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, "Shouldn't be an error"

        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"

    @pytest.mark.parametrize('page_q_params', ["q="+quote('рск')+"&page_size=1", "page=_size=1&q="+quote('рск')])
    def test_q_ignore_incorrect_page_size(self, page_q_params):
        url = 'https://regions-test.2gis.com/1.0/regions?' + page_q_params
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, "Shouldn't be an error"

        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"

    @pytest.mark.parametrize('page_q_params', ["q="+quote('рск')+"&country_code=kz", "country_code=kz&q="+quote('рск')])
    def test_q_ignore_country_code(self, page_q_params):
        url = 'https://regions-test.2gis.com/1.0/regions?' + page_q_params
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"

    @pytest.mark.parametrize('page_q_params', ["q="+quote('рск')+"&country_code=uk", "country_code=uk&q="+quote('рск')])
    def test_q_ignore_incorrect_country_code(self, page_q_params):
        url = 'https://regions-test.2gis.com/1.0/regions?' + page_q_params
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, "Shouldn't be an error"

        itemsList = get_request.get_value_by_key(body, 'items')
        get_request.items_list_shouldnt_be_empty(itemsList)
        gotCityName = get_request.get_value_by_key(itemsList[0], 'name')
        assert len(itemsList) == 5, f"Should have got 5 result, but got {len(itemsList)} instead"


@pytest.mark.page_tests
class TestPageParameter:
    @pytest.mark.parametrize('page_num', ["1", "5", "100", "+25"])
    def test_natural_number_page(self, page_num):
        url = f'https://regions-test.2gis.com/1.0/regions?page={page_num}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, \
            f'Natural page numbers should not cause an error, there is problem with page number {page_num}'

    @pytest.mark.parametrize('page_num', ["0", "-1", "-100"])
    def test_allow_only_natural_number_page(self, page_num):
        url = f'https://regions-test.2gis.com/1.0/regions?page={page_num}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == True, \
            f'Not natural page numbers should cause an error, there is no problem with page number {page_num}'
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')
        
        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_PAGE_MUST_BE_G_THAN_0)

    @pytest.mark.parametrize('page_num', ["four", "15-10+10", quote('twenty three')])
    def test_dont_allow_str_page(self, page_num):
        url = f'https://regions-test.2gis.com/1.0/regions?page={page_num}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == True, \
            f'Not natural page numbers should cause an error, there is no problem with page number {page_num}'
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')
        
        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_PAGE_MUST_BE_NATURAL_NUMBER)


@pytest.mark.country_code_tests
class TestCountryCodeParameter:
    @pytest.mark.parametrize('country_code', ["ru", "kz", "kg", "cz"])
    def test_correct_county_code(self, country_code):
        url = f'https://regions-test.2gis.com/1.0/regions?country_code={country_code}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, \
            f'Error occured with valid country code {country_code}'

    def countryCount(self, country):
        return CountryCount.RU if country == "ru" else CountryCount.KZ if country == "kz" \
            else CountryCount.KG if country == "kg" else CountryCount.CZ

    @pytest.mark.parametrize('country_code', ["ru", "kz", "kg", "cz"])
    def test_correct_county_code_results_count(self, country_code):
        url = f'https://regions-test.2gis.com/1.0/regions?country_code={country_code}&page_size=15'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, \
            f'Error occured with valid country code {country_code}'

        itemsList = get_request.get_value_by_key(body, 'items')
        assert len(itemsList) == self.countryCount(country_code), \
            f"There should be {self.countryCount(country_code)} cities with country code {country_code}"

    @pytest.mark.parametrize('country_code', ["", "ua", "uk", "us"])
    def test_incorrect_county_code(self, country_code):
        url = f'https://regions-test.2gis.com/1.0/regions?country_code={country_code}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()

        body = get_request.make_a_request()
        
        assert get_request.there_is_error(body) == True, \
            f'Invalid country code was processed - {country_code}, valid values are (kz, kg, ru, cz)'
        
        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')
        
        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_INVALID_COUNTRY_CODE)


@pytest.mark.page_size_tests
class TestPageSizeParameter:
    @pytest.mark.parametrize('page_size', ["5", "10", "15"])
    def test_page_size_correct(self, page_size):
        url = f'https://regions-test.2gis.com/1.0/regions?page_size={page_size}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        body = get_request.make_a_request()
        assert get_request.there_is_error(body) == False, "Shouldn't be an error"

    @pytest.mark.parametrize('page_size', ["0", "13", "-1"])
    @pytest.mark.negativetest
    def test_page_size_incorrect_number(self, page_size):
        url = f'https://regions-test.2gis.com/1.0/regions?page_size={quote(page_size)}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, only valid values are 5, 10, 15"

        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')
        
        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_PAGE_SIZE_CAN_BE)

    @pytest.mark.parametrize('page_size', ["", "twenty", "number 4"])
    @pytest.mark.negativetest
    def test_page_size_not_number(self, page_size):
        url = f'https://regions-test.2gis.com/1.0/regions?page_size={quote(page_size)}'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        body = get_request.make_a_request()
        assert get_request.there_is_error(body), "Should be an error, only valid values are 5, 10, 15"

        error = get_request.get_value_by_key(body,'error')
        error_msg = get_request.get_value_by_key(error, 'message')
        
        get_request.should_be_exact_error_msg(error_msg, ErrorMessages.ERROR_PAGE_SIZE_CAN_BE_A_NUMBER)


    @pytest.mark.parametrize('page_size', ["5", "10", "15"])
    def test_pages_count_with_page_size(self, page_size):
        url = f'https://regions-test.2gis.com/1.0/regions?page_size={page_size}&page='
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        nPage = get_request.get_last_page_number(url)
        shouldBeLastPage = 22 // (int)(page_size) if 22 % (int)(page_size) == 0  \
                            else 22 // (int)(page_size) + 1
        assert nPage == shouldBeLastPage, \
            f'Should be {shouldBeLastPage} pages with page_size={page_size}, but there are {nPage} pages'

    @pytest.mark.parametrize('page_size', ["5", "10", "15"])
    def test_items_on_last_page_count_with_page_size(self, page_size):
        url = f'https://regions-test.2gis.com/1.0/regions?page_size={page_size}&page='
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        nPage = get_request.get_last_page_number(url)
        r = 22 % (int)(page_size)
        body = get_request.make_a_request()
        items = get_request.get_value_by_key(body,'items')

        assert len(items) == r, \
            f'Should be {r} items on the last page, but there are {len(items)}'

    def test_default_page_size_should_be_15(self):
        url = f'https://regions-test.2gis.com/1.0/regions'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        body = get_request.make_a_request()
        items = get_request.get_value_by_key(body,'items')

        assert len(items) == 15, \
            f'Should be 15 items on the last page by default, but there are {len(items)}'
    
    def test_default_page_size_with_country_code_parameter_should_be_15(self):
        url = f'https://regions-test.2gis.com/1.0/regions?country_code=ru'
        get_request = InfoPage(url)
        get_request.response_code_should_be_success()
        body = get_request.make_a_request()
        items = get_request.get_value_by_key(body,'items')

        assert len(items) == 13, \
            f"All 13 'ru' items should be seen with default page_size 15, but there are {len(items)}"

