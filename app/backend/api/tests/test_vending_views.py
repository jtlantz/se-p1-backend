import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import VendingMachine  # noqa: E402
from django.test import Client, TestCase  # noqa: E402

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"


class TestVendingMachineCreate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_create_machine_get(self):
        response = self.client.get("/api/machine/add/")
        self.assertEqual(response.status_code, 200)

    def test_create_machine_post(self):
        response = self.client.post(
            "/api/machine/add/",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_add(self):
        response = self.client.put("/api/machine/add/")
        self.assertEqual(response.status_code, 405)


class TestVendingMachineGets(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_get_all_vending_machine(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_get_vending_machine(self):
        response = self.client.get(f"/api/machine/view/{self.vm.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_non_exist_vending_machine(self):
        response = self.client.get(f"/api/machine/view/{self.vm.id+555}")
        self.assertEqual(response.status_code, 404)


class TestVendingMachineUpdate(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_update_vending_machine(self):
        response = self.client.post(
            f"/api/machine/update/{self.vm.id}",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_update_non_exist_vending_machine(self):
        response = self.client.post(
            f"/api/machine/update/{self.vm.id+555}",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        self.assertEqual(response.status_code, 404)


class TestVendingMachineDelete(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_delete_vending_machine(self):
        response = self.client.post(
            f"/api/machine/delete/{self.vm.id}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_non_exist_vending_machine(self):
        response = self.client.post(
            f"/api/machine/delete/{self.vm.id+555}",
        )
        self.assertEqual(response.status_code, 404)
