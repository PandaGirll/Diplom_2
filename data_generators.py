from random import sample

from faker import Faker

fake = Faker()


def generate_user_data():
    return {
        "email": f'panda{fake.email()}',
        "password": fake.password(),
        "name": fake.name()
    }


def generate_order_data(ingredients, count=3):
    return sample([ing['_id'] for ing in ingredients], count)
