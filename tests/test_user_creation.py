import allure
import pytest

from api_methods import ApiMethods
from data_generators import generate_user_data
from expected_responses import *
from helpers import ResponseChecker


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание нового пользователя")
    @pytest.mark.positive
    def test_create_new_user_successfully(self):
        data = generate_user_data()
        response = ApiMethods.register_user(**data)
        assert ResponseChecker.check_status_code(response, SUCCESS_CODE) and \
               ResponseChecker.check_field_exists(response, REGISTER_SUCCESS), \
            f"Ошибка при создании пользователя. Код ответа: {response.status_code}, тело ответа: {response.json()}"

    @allure.title("Попытка создания уже существующего пользователя")
    @pytest.mark.negative
    def test_create_existing_user(self, create_user):
        email, password, name = create_user
        response = ApiMethods.register_user(email=email, password=password, name=name)
        assert ResponseChecker.check_status_code(response, FORBIDDEN_CODE) and \
               ResponseChecker.check_response_field(response, 'message', REGISTER_USER_EXISTS['message']), \
            (f"Неожиданный ответ при попытке создать существующего пользователя. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")

    @allure.title("Попытка создания пользователя без обязательного поля")
    @pytest.mark.negative
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, field):
        data = generate_user_data()
        data[field] = ""
        response = ApiMethods.register_user(**data)
        assert ResponseChecker.check_status_code(response, FORBIDDEN_CODE) and \
               ResponseChecker.check_response_field(response, 'message', REGISTER_MISSING_FIELD['message']), \
            (f"Неожиданный ответ при попытке создать пользователя без {field}. "
             f"Код ответа: {response.status_code}, тело ответа: {response.json()}")
