import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from django.test import RequestFactory, TestCase  # noqa: E402

TEST_MACHINE = "test machine"
TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"
TEST_ON_HAND = 50
TEST_PRICE = 1.00
TEST_PRODUCT = "test product"

from api.views import (  # noqa: E402
    add_vending_machine,
    delete_vending_machine,
    get_all_machines,
    get_machine,
    update_vending_machine,
)


class TestVendingMachineEndpoints(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)

    def test_create_machine_get(self):
        request = self.request_factory.get("/api/machine/add/")
        request = add_vending_machine(request)
        self.assertEqual(request.status_code, 200)

    def test_create_machine_post(self):
        request = self.request_factory.post(
            "/api/machine/add/",
            {
                "building": TEST_MACHINE,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        response = add_vending_machine(request)
        self.assertEqual(response.status_code, 200)

    def test_get_all_vending_machine(self):
        request = self.request_factory.get("/api/")
        response = get_all_machines(request)
        self.assertEqual(response.status_code, 200)

    def test_get_vending_machine(self):
        request = self.request_factory.get("/api/machine/1/")
        response = get_machine(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_update_vending_machine(self):
        request = self.request_factory.post(
            "/api/machine/update/1/",
            {
                "building": TEST_MACHINE,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        response = update_vending_machine(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_vending_machine(self):
        request = self.request_factory.post("/api/machine/delete/1/")
        response = delete_vending_machine(request, 1)
        self.assertEqual(response.status_code, 200)


from api.views import add_product, delete_product, get_all_products, get_product, update_product  # noqa: E402

TEST_PRODUCT_NAME = "test product"
TEST_PRODUCT_PRICE = 1.00
TEST_PRODUCT_ON_HAND = 50


class TestProductEndpoints(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)

    def test_create_product_get(self):
        request = self.request_factory.get("/api/product/add/")
        request = add_product(request)
        self.assertEqual(request.status_code, 200)

    def test_create_product_post(self):
        request = self.request_factory.post(
            "/api/product/add/",
            {
                "name": TEST_PRODUCT_NAME,
                "price": TEST_PRODUCT_PRICE,
                "on_hand": TEST_PRODUCT_ON_HAND,
            },
        )
        response = add_product(request)
        self.assertEqual(response.status_code, 200)

    def test_get_all_products(self):
        request = self.request_factory.get("/api/product/")
        response = get_all_products(request)
        self.assertEqual(response.status_code, 200)

    def test_get_product(self):
        request = self.request_factory.get("/api/product/1/")
        response = get_product(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        request = self.request_factory.post(
            "/api/product/update/1/",
            {
                "price": TEST_PRODUCT_PRICE,
                "on_hand": TEST_PRODUCT_ON_HAND,
            },
        )
        response = update_product(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        request = self.request_factory.post("/api/product/delete/1/")
        response = delete_product(request, 1)
        self.assertEqual(response.status_code, 200)


from api.views import add_stock, delete_stock, get_all_stock, get_stock, update_stock  # noqa: E402

TEST_STOCK_MACHINE = 1
TEST_STOCK_PRODUCT = 1
TEST_STOCK_QUANTITY = 20


class TestStockEndpoints(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)

        request = self.request_factory.post(
            "/api/machine/add/",
            {
                "building": TEST_MACHINE,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        add_vending_machine(request)
        request = self.request_factory.post(
            "/api/product/add/",
            {
                "name": TEST_PRODUCT_NAME,
                "price": TEST_PRODUCT_PRICE,
                "on_hand": TEST_PRODUCT_ON_HAND,
            },
        )
        add_product(request)

    def test_create_stock_get(self):
        request = self.request_factory.get("/api/stock/add/")
        request = add_stock(request)
        self.assertEqual(request.status_code, 200)

    def test_create_stock_post(self):
        request = self.request_factory.post(
            "/api/stock/add/",
            {
                "vending_machine": 1,
                "product": 1,
                "quantity": TEST_STOCK_QUANTITY,
            },
        )
        response = add_stock(request)
        response.status_code
        # self.assertEqual(response.status_code, 200)

    def test_get_all_stock(self):
        request = self.request_factory.get("/api/stock/")
        response = get_all_stock(request)
        self.assertEqual(response.status_code, 200)

    def test_get_stock(self):
        request = self.request_factory.get("/api/stock/1/")
        response = get_stock(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_update_stock(self):
        request = self.request_factory.post(
            "/api/stock/update/1/",
            {
                "quantity": TEST_STOCK_QUANTITY,
            },
        )
        response = update_stock(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_stock(self):
        request = self.request_factory.post("/api/stock/delete/1/")
        response = delete_stock(request, 1)
        self.assertEqual(response.status_code, 200)
