import allure
import pytest

from api_methods import ApiMethods
from data_generators import generate_user_data
from expected_responses import *
from helpers import ResponseChecker


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:

    @allure.title("Успешное изменение данных авторизованного пользователя")
    @pytest.mark.positive
    @pytest.mark.parametrize('update_field', ['email', 'name'])
    def test_update_authorized_user(self, new_user, update_field):
        new_data = generate_user_data()
        payload = {update_field: new_data[update_field]}
        response = ApiMethods.update_user(new_user['access_token'], **payload)
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_user_field(response, update_field, new_data[update_field]), \
            (f"Не удалось обновить {update_field} пользователя. "
             f"Получено: {response.status_code} {response.json()['user'][update_field]}. "
             f"Ожидалось: {SUCCESS_CODE} {new_data[update_field]}")

    @allure.title("Попытка изменения данных неавторизованного пользователя")
    @pytest.mark.negative
    @pytest.mark.parametrize("field", ["email", "name"])
    def test_update_unauthorized_user(self, field):
        new_data = generate_user_data()
        response = ApiMethods.update_user("", **{field: new_data[field]})
        assert ResponseChecker.check_status_code(response, UNAUTHORIZED_CODE) and \
               ResponseChecker.check_response_field(response, 'message', UPDATE_USER_UNAUTHORIZED['message']), \
            (f"Неожиданный ответ при попытке обновления данных неавторизованного пользователя. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    @allure.title("Попытка обновления email на уже существующий")
    @pytest.mark.negative
    def test_update_to_existing_email(self, new_user):
        existing_email = 'test@email.ru'
        response = ApiMethods.update_user(new_user['access_token'], email=existing_email)

        assert ResponseChecker.check_status_code(response, FORBIDDEN_CODE) and \
               ResponseChecker.check_response_field(response, 'message', "User with such email already exists"), \
            (f"Неожиданный ответ при попытке обновления на существующий email. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")
