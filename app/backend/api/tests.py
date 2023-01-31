from django.test import TestCase

from .views import *
from .models import *


# Create your tests here.

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"


class TestCreateVendingMachine(TestCase):

    def setUp(self):
        vm = VendingMachine(building=TEST_BUILDING, floor=TEST_FLOOR, location=TEST_LOCATION)
        vm.save()


    def test_vending_machine_created(self):
        vm = VendingMachine.objects.get(building=TEST_BUILDING)
        self.assertTrue(vm.building == TEST_BUILDING)
        self.assertTrue(vm.floor == TEST_FLOOR)
        self.assertTrue(vm.location == TEST_LOCATION)


TEST_PRODUCT = "test product"
TEST_PRICE = 1.00
TEST_ON_HAND = 1

class TestCreateProduct(TestCase):

    def setUp(self):
        product = Product(name=TEST_PRODUCT, price=TEST_PRICE, on_hand=TEST_ON_HAND)
        product.save()

    def test_product_created(self):
        product = Product.objects.get(name=TEST_PRODUCT)
        self.assertTrue(product.name == TEST_PRODUCT)
        self.assertTrue(product.price == TEST_PRICE)
        self.assertTrue(product.on_hand == TEST_ON_HAND)

TEST_QUANTITY = 1
class TestCreateStock(TestCase):
    
        def setUp(self):
            vm = VendingMachine(building=TEST_BUILDING, floor=TEST_FLOOR, location=TEST_LOCATION)
            vm.save()
            product = Product(name=TEST_PRODUCT, price=TEST_PRICE, on_hand=TEST_ON_HAND)
            product.save()
            stock = Stock(vending_machine=vm, product_info=product, quantity=TEST_QUANTITY)
            stock.save()
    
        def test_stock_created(self):
            stock = Stock.objects.get(product_info__name=TEST_PRODUCT)
            self.assertTrue(stock.quantity == TEST_QUANTITY)
            self.assertTrue(stock.vending_machine.building == TEST_BUILDING)
            self.assertTrue(stock.product_info.name == TEST_PRODUCT)