import allure
import requests

from endpoints import *


class ApiMethods:
    @staticmethod
    @allure.step("Регистрация пользователя: {email}")
    def register_user(email, password, name):
        data = {"email": email, "password": password, "name": name}
        return requests.post(REGISTER, json=data)

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(email, password):
        data = {"email": email, "password": password}
        return requests.post(LOGIN, json=data)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(token):
        headers = {'Authorization': token}
        return requests.delete(USER, headers=headers)

    @staticmethod
    @allure.step("Изменение данных пользователя")
    def update_user(token, **data):
        headers = {'Authorization': token}
        return requests.patch(USER, json=data, headers=headers)

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients():
        return requests.get(INGREDIENTS)

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(token, ingredients):
        headers = {'Authorization': token}
        data = {"ingredients": ingredients}
        return requests.post(ORDERS, json=data, headers=headers)

    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_user_orders(token):
        headers = {'Authorization': token}
        return requests.get(ORDERS, headers=headers)
