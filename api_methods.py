import requests
import allure
from endpoints import *


@allure.step("Регистрация пользователя")
def register_user(email, password, name):
    data = {"email": email, "password": password, "name": name}
    return requests.post(REGISTER, json=data)


@allure.step("Авторизация пользователя")
def login_user(email, password):
    data = {"email": email, "password": password}
    return requests.post(LOGIN, json=data)


@allure.step("Удаление пользователя")
def delete_user(email, password):
    token = login_user(email, password).json()['accessToken']
    headers = {'Authorization': token}
    return requests.delete(USER, headers=headers)


@allure.step("Изменение данных пользователя")
def update_user(token, **data):
    headers = {'Authorization': token}
    return requests.patch(USER, json=data, headers=headers)


@allure.step("Получение списка ингредиентов")
def get_ingredients():
    return requests.get(INGREDIENTS)


@allure.step("Создание заказа")
def create_order(token, ingredients):
    headers = {'Authorization': token}
    data = {"ingredients": ingredients}
    return requests.post(ORDERS, json=data, headers=headers)


@allure.step("Получение заказов пользователя")
def get_user_orders(token):
    headers = {'Authorization': token}
    return requests.get(ORDERS, headers=headers)
