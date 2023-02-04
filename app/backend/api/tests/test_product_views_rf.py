import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import Product  # noqa: E402
from django.http import Http404  # noqa: E402
from django.test import RequestFactory, TestCase  # noqa: E402

TEST_ON_HAND = 50
TEST_PRICE = 1.00
TEST_PRODUCT = "test product"

from api.views import add_product, delete_product, get_all_products, get_product, update_product  # noqa: E402


class TestProductCreate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )

    def test_create_product_get(self):
        request = self.request_factory.get("/api/product/add/")
        response = add_product(request)
        self.assertEqual(response.status_code, 200)

    def test_create_product_post(self):
        request = self.request_factory.post(
            "/api/product/add/",
            data={
                "name": TEST_PRODUCT,
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )
        response = add_product(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_add_product_method(self):
        request = self.request_factory.put("/api/product/add/")
        response = add_product(request)
        self.assertEqual(response.status_code, 405)


class TestProductGets(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_get_all_products(self):
        request = self.request_factory.get("/api/product/view/")
        response = get_all_products(request)
        self.assertEqual(response.status_code, 200)

    def test_get_product(self):
        request = self.request_factory.get(f"/api/product/view/{self.product.id}")
        response = get_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_get_product_not_found(self):
        request = self.request_factory.get(f"/api/product/view/{self.product.id + 555}")
        with self.assertRaises(Http404):
            get_product(request, self.product.id + 555)


class TestProductUpdate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_update_product_get(self):
        request = self.request_factory.get(f"/api/product/update/{self.product.id}")
        response = update_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_update_product_post(self):
        request = self.request_factory.post(
            f"/api/product/update/{self.product.id}",
            data={
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )
        response = update_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_update_product_not_found(self):
        request = self.request_factory.post(
            f"/api/product/update/{self.product.id + 555}",
            data={
                "price": TEST_PRICE,
                "on_hand": TEST_ON_HAND,
            },
        )
        with self.assertRaises(Http404):
            update_product(request, self.product.id + 555)

    def test_invalid_update_product_method(self):
        request = self.request_factory.put(f"/api/product/update/{self.product.id}")
        response = update_product(request, self.product.id)
        self.assertEqual(response.status_code, 405)


class TestProductDelete(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.product = Product(
            name=TEST_PRODUCT,
            price=TEST_PRICE,
            on_hand=TEST_ON_HAND,
        )
        self.product.save()

    def test_delete_product_post(self):
        request = self.request_factory.post(f"/api/product/delete/{self.product.id}")
        response = delete_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_product_not_found(self):
        request = self.request_factory.post(f"/api/product/delete/{self.product.id + 555}")
        with self.assertRaises(Http404):
            delete_product(request, self.product.id + 555)

    def test_invalid_delete_product_method(self):
        request = self.request_factory.put(f"/api/product/delete/{self.product.id}")
        response = delete_product(request, self.product.id)
        self.assertEqual(response.status_code, 405)
