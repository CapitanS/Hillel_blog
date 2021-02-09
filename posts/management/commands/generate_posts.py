import json

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from faker.generator import random


def generate_city() -> str:
    """
        Generate random city
        @return: str with city_name
        """
    fake = Faker(['en_US'])
    city_name = fake.city()

    return city_name


def generate_product() -> dict:
    """
        Generate random product
        @return: dict with product_name and his price
        """
    dict_product = {
        'product_name': '',
        'product_price': '',
    }
    fake = Faker(['en_US'])
    product_name = fake.word()
    product_price = round(random.uniform(0.9, 225.9), 2)
    dict_product['product_name'] = product_name
    dict_product['product_price'] = product_price
    return dict_product


def generate_customers(number: int) -> dict:
    """
    Generate random customer
    @return: dictionary with first_name, last_name, city_id, product_id
    """
    dict_user = {
        'first_name': '',
        'last_name': '',
        'city': '',
        'product': []
    }
    fake = Faker(['en_US'])
    first_name = fake.first_name()
    last_name = fake.last_name()
    city_id = random.randint(1, number)

    dict_user['first_name'] = first_name
    dict_user['last_name'] = last_name
    dict_user['city'] = city_id
    for _ in range(random.randint(1, 3)):
        dict_user['product'].append(random.randint(1, number))

    return dict_user


class Command(BaseCommand):
    help = "Create random city, customer, products"  # noqa:A003

    def add_arguments(self, parser):
        parser.add_argument('instance_number', type=int, help='Number of generated instance')

    def handle(self, *args, **kwargs):
        instance_number = kwargs['instance_number']

        # Generate base of cities to json file for loaddata
        cities_base = []
        for n in range(1, instance_number + 1):
            city_name = generate_city()
            city_instance = {
                "model": "orders.city",
                "pk": n,
                "fields": {
                    "name": city_name
                }
            }
            cities_base.append(city_instance)
        try:
            with open('orders/fixtures/orders_city.json', 'w') as cities:
                json.dump(cities_base, cities)
        except Exception as err:
            raise CommandError('Some error occurred:', str(err))

        # Generate base of products to json file for loaddata
        products_base = []
        for n in range(1, instance_number + 1):
            product = generate_product()
            product_instance = {
                "model": "orders.product",
                "pk": n,
                "fields": {
                    "name": product['product_name'],
                    "price": product['product_price']
                }
            }
            products_base.append(product_instance)
        try:
            with open('orders/fixtures/orders_product.json', 'w') as products:
                json.dump(products_base, products)
        except Exception as err:
            raise CommandError('Some error occurred:', str(err))

        # Generate base of customers to json file for loaddata
        customers_base = []
        for n in range(1, instance_number + 1):
            customer = generate_customers(instance_number)
            customer_instance = {
                "model": "orders.customer",
                "pk": n,
                "fields": {
                    "first_name": customer['first_name'],
                    "last_name": customer['last_name'],
                    "city": customer['city'],
                    "product": customer['product'],
                }
            }
            customers_base.append(customer_instance)
        try:
            with open('orders/fixtures/orders_customer.json', 'w') as customers:
                json.dump(customers_base, customers)
        except Exception as err:
            raise CommandError('Some error occurred:', str(err))
