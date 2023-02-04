import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import VendingMachine  # noqa: E402
from django.http import Http404  # noqa: E402
from django.test import RequestFactory, TestCase  # noqa: E402

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"

from api.views import (  # noqa: E402
    add_vending_machine,
    delete_vending_machine,
    get_all_machines,
    get_machine,
    update_vending_machine,
)


class TestVendingMachineCreate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)

    def test_create_machine_get(self):
        request = self.request_factory.get("/api/machine/add/")
        response = add_vending_machine(request)
        self.assertEqual(response.status_code, 200)

    def test_create_machine_post(self):
        request = self.request_factory.post(
            "/api/machine/add/",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        response = add_vending_machine(request)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_add(self):
        request = self.request_factory.put("/api/machine/add/")
        response = add_vending_machine(request)
        self.assertEqual(response.status_code, 405)


class TestVendingMachineGets(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_get_all_vending_machine(self):
        request = self.request_factory.get("/api/")
        response = get_all_machines(request)
        self.assertEqual(response.status_code, 200)

    def test_get_vending_machine(self):
        request = self.request_factory.get(f"/api/machine/view/{self.vm.id}")
        response = get_machine(request, self.vm.id)
        self.assertEqual(response.status_code, 200)

    def test_get_non_exist_vending_machine(self):
        request = self.request_factory.get(f"/api/machine/view/{self.vm.id+555}")
        with self.assertRaises(Http404):
            get_machine(request, self.vm.id + 555)


class TestVendingMachineUpdate(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_update_vending_machine(self):
        request = self.request_factory.post(
            f"/api/machine/update/{self.vm.id}",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        response = update_vending_machine(request, self.vm.id)
        self.assertEqual(response.status_code, 200)

    def test_update_non_exist_vending_machine(self):
        request = self.request_factory.post(
            f"/api/machine/update/{self.vm.id+555}",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        with self.assertRaises(Http404):
            update_vending_machine(request, self.vm.id + 555)

    def test_update_invalid_put_request(self):
        request = self.request_factory.put(
            f"/api/machine/update/{self.vm.id}",
            data={
                "building": TEST_BUILDING,
                "floor": TEST_FLOOR,
                "location": TEST_LOCATION,
            },
        )
        response = update_vending_machine(request, self.vm.id)
        self.assertEqual(response.status_code, 405)


class TestVendingMachineDelete(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory(enforce_csrf_checks=False)
        self.vm = VendingMachine(
            building=TEST_BUILDING,
            floor=TEST_FLOOR,
            location=TEST_LOCATION,
        )
        self.vm.save()

    def test_delete_vending_machine(self):
        request = self.request_factory.post(
            f"/api/machine/delete/{self.vm.id}",
        )
        response = delete_vending_machine(request, self.vm.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_non_exist_vending_machine(self):
        request = self.request_factory.post(
            f"/api/machine/delete/{self.vm.id+555}",
        )
        with self.assertRaises(Http404):
            delete_vending_machine(request, self.vm.id + 555)

    def test_delete_invalid_put_request(self):
        request = self.request_factory.put(
            f"/api/machine/delete/{self.vm.id}",
        )
        response = delete_vending_machine(request, self.vm.id)
        self.assertEqual(response.status_code, 405)
