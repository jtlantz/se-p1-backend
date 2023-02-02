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

from api.views import add_vending_machine  # noqa: E402


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
