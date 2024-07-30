import pytest
import allure
from api_methods import get_user_orders, create_order
from data_generators import generate_order_data
from expected_responses import *
from helpers import ResponseChecker

@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Успешное получение заказов авторизованным пользователем")
    @pytest.mark.positive
    def test_get_orders_authorized(self, new_user, ingredients):
        # Создаем заказ для пользователя
        order_data = generate_order_data(ingredients)
        create_order(new_user['access_token'], order_data)

        response = get_user_orders(new_user['access_token'])
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_field_exists(response, 'orders'), \
            f"Не удалось получить заказы пользователя. Код ответа: {response.status_code}, тело ответа: {response.json()}"
        assert len(response.json()['orders']) > 0, "Список заказов пуст"

    @allure.title("Попытка получения заказов неавторизованным пользователем")
    @pytest.mark.negative
    def test_get_orders_unauthorized(self):
        response = get_user_orders("")
        assert ResponseChecker.check_status_code(response, UNAUTHORIZED_CODE) and \
               ResponseChecker.check_response_field(response, 'message', GET_ORDERS_UNAUTHORIZED['message']), \
            f"Неожиданный ответ при попытке получения заказов неавторизованным пользователем. Код ответа: {response.status_code}, тело ответа: {response.json()}"
