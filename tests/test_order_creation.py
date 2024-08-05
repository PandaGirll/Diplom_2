import allure
import pytest

from api_methods import ApiMethods
from data_generators import generate_order_data
from expected_responses import *
from helpers import ResponseChecker


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Успешное создание заказа авторизованным пользователем")
    @pytest.mark.positive
    def test_create_order_authorized(self, new_user, ingredients):
        order_data = generate_order_data(ingredients)
        response = ApiMethods.create_order(new_user['access_token'], order_data)
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_field_exists(response, 'order'), \
            f"Не удалось создать заказ. Код ответа: {response.status_code}, тело ответа: {response.json()}"

    @allure.title("Попытка создания заказа неавторизованным пользователем")
    @allure.description("""
        Известный баг: API позволяет создать заказ неавторизованному пользователю.
        Ожидаемое поведение: код ответа 401 Unauthorized.
        Фактическое поведение: код ответа 200, заказ создаётся.
    """)
    @pytest.mark.negative
    def test_create_order_unauthorized(self, ingredients):
        order_data = generate_order_data(ingredients)
        response = ApiMethods.create_order("", order_data)
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_response_field(response, 'success', CREATE_ORDER_SUCCESS['success']), \
            (f"Неожиданный ответ при попытке создания заказа неавторизованным пользователем. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    @allure.title("Попытка создания заказа без ингредиентов")
    @pytest.mark.negative
    def test_create_order_without_ingredients(self, new_user):
        response = ApiMethods.create_order(new_user['access_token'], [])
        assert ResponseChecker.check_status_code(response, BAD_REQUEST_CODE) and \
               ResponseChecker.check_response_field(response, 'message', CREATE_ORDER_NO_INGREDIENTS['message']), \
            (f"Неожиданный ответ при попытке создания заказа без ингредиентов. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    @allure.title("Попытка создания заказа с неверным хешем ингредиентов")
    @pytest.mark.negative
    def test_create_order_with_invalid_ingredients(self, new_user):
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        response = ApiMethods.create_order(new_user['access_token'], invalid_ingredients)
        assert ResponseChecker.check_status_code(response, SERVER_ERROR_CODE), \
            (f"Неожиданный ответ при попытке создания заказа с неверным хешем ингредиентов. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")
