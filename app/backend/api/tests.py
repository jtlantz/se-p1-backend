from django.test import TestCase
from .views import *
from .models import *

# Create your tests here.

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"


class TestCreateVendingMachine(TestCase):

    def setUp(self):
        VendingMachine(building=TEST_BUILDING, floor=TEST_FLOOR, location=TEST_LOCATION)

    def test_vending_machine_created(self):
        vm = VendingMachine.objects.filter(building="Test Building")
        self.assertTrue(vm.building == TEST_BUILDING)
        self.assertTrue(vm.floor == TEST_FLOOR)
        self.assertTrue(vm.location == TEST_LOCATION)
        vm.delete()
