import allure


class ResponseChecker:
    @staticmethod
    def check_status_code(response, expected_status_code):
        with allure.step(f'Проверяем код ответа. Код ответа - {response.status_code}'):
            return response.status_code == expected_status_code

    @staticmethod
    def check_response_field(response, field, expected_value):
        with allure.step(
                f"Проверяем значение поля '{field}' в ответе ({response.json().get(field, 'Поле отсутствует')})"):
            return response.json().get(field) == expected_value

    @staticmethod
    def check_user_field(response, field, expected_value):
        with allure.step(
                f"Проверяем значение поля '{field}' пользователя в ответе ({response.json().get('user', {}).get(field, 'Поле отсутствует')})"):
            return response.json().get('user', {}).get(field) == expected_value

    @staticmethod
    def check_field_exists(response, field):
        with allure.step(f"Проверяем наличие поля '{field}' в ответе"):
            return field in response.json()
