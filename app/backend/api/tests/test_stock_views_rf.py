import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import Product, Stock, VendingMachine  # noqa: E402
from django.http import Http404  # noqa: E402
from django.test import RequestFactory, TestCase  # noqa: E402

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"
TEST_ON_HAND = 50
TEST_PRICE = 1.00
TEST_PRODUCT = "test product"
TEST_QUANTITY = 4

from api.views import add_stock, delete_stock, get_all_stock, get_stock, update_stock  # noqa: E402, F401, F403


class TestStockCreate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
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
        request = self.request_factory.get("/api/stock/add/")
        response = add_stock(request)
        self.assertEqual(response.status_code, 200)

    def test_create_stock_post(self):
        request = self.request_factory.post(
            "/api/stock/add/",
            data={
                "product": self.product.id,
                "vending_machine": self.vending_machine.id,
                "quantity": TEST_QUANTITY,
            },
        )
        response = add_stock(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_add_stock_method(self):
        request = self.request_factory.put("/api/stock/add/")
        response = add_stock(request)
        self.assertEqual(response.status_code, 405)


class TestStockGets(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
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
        request = self.request_factory.get("/api/stock/view/")
        response = get_all_stock(request)
        self.assertEqual(response.status_code, 200)

    def test_get_stock_by_id(self):
        request = self.request_factory.get(f"/api/stock/view/{self.stock.id}")
        response = get_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_stock(self):
        request = self.request_factory.get(f"/api/stock/view/{self.stock.id + 555}")
        with self.assertRaises(Http404):
            get_stock(request, self.stock.id + 555)


class TestStockUpdate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
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
        request = self.request_factory.get(f"/api/stock/update/{self.stock.id}")
        response = update_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 200)

    def test_update_stock_post(self):
        request = self.request_factory.post(
            f"/api/stock/update/{self.stock.id}",
            data={
                "product": self.product.id,
                "vending_machine": self.vending_machine.id,
                "quantity": TEST_QUANTITY,
            },
        )
        response = update_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_stock_method(self):
        request = self.request_factory.put(f"/api/stock/update/{self.stock.id}")
        response = update_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 405)


class TestStockDelete(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
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
        request = self.request_factory.post(f"/api/stock/delete/{self.stock.id}")
        response = delete_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_delete_stock_method(self):
        request = self.request_factory.put(f"/api/stock/delete/{self.stock.id}")
        response = delete_stock(request, self.stock.id)
        self.assertEqual(response.status_code, 405)
