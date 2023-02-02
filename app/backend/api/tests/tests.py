import os

import django  # noqa: E402

# These imports must be done in this order in order for tests to run properly

os.environ.setdefault("POSTGRES_DB", "localhost")  # noqa: E402
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"  # noqa: E402
django.setup()  # noqa: E402

from api.models import Product, Stock, VendingMachine  # noqa: E402
from django.test import TestCase  # noqa: E402

# Create your tests here.

TEST_BUILDING = "test building"
TEST_FLOOR = 1
TEST_LOCATION = "test room"


class TestCreateVendingMachine(TestCase):  # noqa: D103
    def setUp(self):  # noqa: D103
        vm = VendingMachine(building=TEST_BUILDING, floor=TEST_FLOOR, location=TEST_LOCATION)
        vm.save()

    def test_vending_machine_created(self):  # noqa: D103
        vm = VendingMachine.objects.get(building=TEST_BUILDING)
        self.assertTrue(vm.building == TEST_BUILDING)
        self.assertTrue(vm.floor == TEST_FLOOR)
        self.assertTrue(vm.location == TEST_LOCATION)

    def test_vending_machine_str(self):  # noqa: D103
        vm = VendingMachine.objects.get(building=TEST_BUILDING)
        self.assertEqual(
            str(vm),
            f"""\
id: {vm.id}, \
building: {TEST_BUILDING}, \
floor: {TEST_FLOOR}, \
location: {TEST_LOCATION}\
""",
        )

    def test_vending_machine_repr(self):  # noqa: D103
        vm = VendingMachine.objects.get(building=TEST_BUILDING)
        self.assertEqual(
            repr(vm),
            f"""\
id: {vm.id}, \
building: {TEST_BUILDING}, \
floor: {TEST_FLOOR}, \
location: {TEST_LOCATION}\
""",
        )


TEST_PRODUCT = "test product"
TEST_PRICE = 1.00
TEST_ON_HAND = 1


class TestCreateProduct(TestCase):  # noqa: D103
    def setUp(self):  # noqa: D103
        product = Product(name=TEST_PRODUCT, price=TEST_PRICE, on_hand=TEST_ON_HAND)
        product.save()

    def test_product_created(self):  # noqa: D103
        product = Product.objects.get(name=TEST_PRODUCT)
        self.assertTrue(product.name == TEST_PRODUCT)
        self.assertTrue(product.price == TEST_PRICE)
        self.assertTrue(product.on_hand == TEST_ON_HAND)

    def test_product_str(self):  # noqa: D103
        product = Product.objects.get(name=TEST_PRODUCT)
        self.assertEqual(
            str(product),
            f"""\
id: {product.id}, \
name: {TEST_PRODUCT}, \
price: 1.00, \
on_hand: {TEST_ON_HAND}\
""",
        )

    def test_product_repr(self):  # noqa: D103
        product = Product.objects.get(name=TEST_PRODUCT)
        self.assertEqual(
            repr(product),
            f"""\
id: {product.id}, \
name: {TEST_PRODUCT}, \
price: 1.00, \
on_hand: {TEST_ON_HAND}\
""",
        )


TEST_QUANTITY = 1


class TestCreateStock(TestCase):  # noqa: D103
    def setUp(self):  # noqa: D103
        vm = VendingMachine(building=TEST_BUILDING, floor=TEST_FLOOR, location=TEST_LOCATION)
        vm.save()
        product = Product(name=TEST_PRODUCT, price=TEST_PRICE, on_hand=TEST_ON_HAND)
        product.save()
        stock = Stock(vending_machine=vm, product_info=product, quantity=TEST_QUANTITY)
        stock.save()

    def test_stock_created(self):  # noqa: D103
        stock = Stock.objects.get(product_info__name=TEST_PRODUCT)
        self.assertTrue(stock.quantity == TEST_QUANTITY)
        self.assertTrue(stock.vending_machine.building == TEST_BUILDING)
        self.assertTrue(stock.product_info.name == TEST_PRODUCT)

    def test_stock_str(self):  # noqa: D103
        stock = Stock.objects.get(product_info__name=TEST_PRODUCT)
        self.assertEqual(
            str(stock),
            f"""\
id: {stock.id}, \
product_info: { {stock.product_info} }, \
quantity: {stock.quantity}, \
location: { {stock.vending_machine} }\
""",
        )

    def test_stock_repr(self):  # noqa: D103
        stock = Stock.objects.get(product_info__name=TEST_PRODUCT)
        self.assertEqual(
            repr(stock),
            f"""\
id: {stock.id}, \
product_info: { {stock.product_info} }, \
quantity: {stock.quantity}, \
location: { {stock.vending_machine} }\
""",
        )

    def test_stock_update_quantity(self):  # noqa: D103
        stock = Stock.objects.get(product_info__name=TEST_PRODUCT)
        stock.update_quantity(5)
        self.assertEqual(stock.quantity, 5)
