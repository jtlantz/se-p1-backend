import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import Product, Stock, VendingMachine  # noqa: E402
from django.test import Client, TestCase  # noqa: E402

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"
TEST_ON_HAND = 50
TEST_PRICE = 1.00
TEST_PRODUCT = "test product"
TEST_QUANTITY = 4


class TestStockCreate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()
        self.vending_machine = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vending_machine.save()

        self.stock = Stock(
            product_info=self.product,
            vending_machine=self.vending_machine,
            quantity=TEST_QUANTITY,
        )
        self.stock.save()

    def test_create_stock_get(self):
        response = self.client.get("/api/stock/add/")
        self.assertEqual(response.status_code, 200)

    def test_create_stock_post(self):
        response = self.client.post(
            "/api/stock/add/",
            data={
                "product": self.product.id,
                "vending_machine": self.vending_machine.id,
                "quantity": TEST_QUANTITY,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_add_stock_method(self):
        response = self.client.put("/api/stock/add/")
        self.assertEqual(response.status_code, 405)


class TestStockGets(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()
        self.vending_machine = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vending_machine.save()

        self.stock = Stock(
            product_info=self.product,
            vending_machine=self.vending_machine,
            quantity=TEST_QUANTITY,
        )
        self.stock.save()

    def test_get_all_stocks(self):
        response = self.client.get("/api/stock/view/")
        self.assertEqual(response.status_code, 200)

    def test_get_stock_by_id(self):
        response = self.client.get(f"/api/stock/view/{self.stock.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_stock(self):
        response = self.client.get(f"/api/stock/view/{self.stock.id + 555}")
        self.assertEqual(response.status_code, 404)


class TestStockUpdate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()
        self.vending_machine = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vending_machine.save()

        self.stock = Stock(
            product_info=self.product,
            vending_machine=self.vending_machine,
            quantity=TEST_QUANTITY,
        )
        self.stock.save()

    def test_update_stock_get(self):
        response = self.client.get(f"/api/stock/update/{self.stock.id}")
        self.assertEqual(response.status_code, 200)

    def test_update_stock_post(self):
        response = self.client.post(
            f"/api/stock/update/{self.stock.id}",
            data={
                "product": self.product.id,
                "vending_machine": self.vending_machine.id,
                "quantity": TEST_QUANTITY,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_stock_method(self):
        response = self.client.put(f"/api/stock/update/{self.stock.id}")
        self.assertEqual(response.status_code, 405)


class TestStockDelete(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()
        self.vending_machine = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vending_machine.save()

        self.stock = Stock(
            product_info=self.product,
            vending_machine=self.vending_machine,
            quantity=TEST_QUANTITY,
        )
        self.stock.save()

    def test_delete_stock_post(self):
        response = self.client.post(f"/api/stock/delete/{self.stock.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_delete_stock_method(self):
        response = self.client.put(f"/api/stock/delete/{self.stock.id}")
        self.assertEqual(response.status_code, 405)
