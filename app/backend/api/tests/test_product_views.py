import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import Product  # noqa: E402
from django.test import Client, TestCase  # noqa: E402

TEST_ON_HAND = 50
TEST_PRICE = 1.00
TEST_PRODUCT = "test product"


class TestProductCreate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )

    def test_create_product_get(self):
        response = self.client.get("/api/product/add/")
        self.assertEqual(response.status_code, 200)

    def test_create_product_post(self):
        response = self.client.post(
            "/api/product/add/",
            data={
                "name": TEST_PRODUCT,
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_add_product_method(self):
        response = self.client.put("/api/product/add/")
        self.assertEqual(response.status_code, 405)


class TestProductGets(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_get_all_products(self):
        response = self.client.get("/api/product/view/")
        self.assertEqual(response.status_code, 200)

    def test_get_product(self):
        response = self.client.get(f"/api/product/view/{self.product.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_product_not_found(self):
        response = self.client.get(f"/api/product/view/{self.product.id + 555}")
        self.assertEqual(response.status_code, 404)


class TestProductUpdate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_update_product_get(self):
        response = self.client.get(f"/api/product/update/{self.product.id}")
        self.assertEqual(response.status_code, 200)

    def test_update_product_post(self):
        response = self.client.post(
            f"/api/product/update/{self.product.id}",
            data={
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_update_product_not_found(self):
        response = self.client.post(
            f"/api/product/update/{self.product.id + 555}",
            data={
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_update_product_method(self):
        response = self.client.put(f"/api/product/update/{self.product.id}")
        self.assertEqual(response.status_code, 405)


class TestProductDelete(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_delete_product_post(self):
        response = self.client.post(f"/api/product/delete/{self.product.id}")
        self.assertEqual(response.status_code, 200)

    def test_delete_product_not_found(self):
        response = self.client.post(f"/api/product/delete/{self.product.id + 555}")
        self.assertEqual(response.status_code, 404)

    def test_invalid_delete_product_method(self):
        response = self.client.put(f"/api/product/delete/{self.product.id}")
        self.assertEqual(response.status_code, 405)
