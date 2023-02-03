from django.db import models
from django.forms.models import model_to_dict


class VendingMachine(models.Model):
    """
    Vending machine class model for database.

    Each vending machine is defined here.
    Create the vending machine with the building, floor and location
    Args:
        building (str): The building name
        floor (int): The floor number
        location (str): The room number

    Class Attributes:
        id (int): The id of the vending machine is automatically assigned
        building (str): The building name
        floor (int): The floor number
        location (str): The room number
    """

    id = models.AutoField(primary_key=True, unique=True)
    building = models.CharField(max_length=50)
    floor = models.IntegerField()
    location = models.CharField(max_length=50)

    def as_dict(self) -> dict:
        """
        Return the vending machine as a dictionary.

        Returns:
            dict: The vending machine as a dictionary
        """
        return model_to_dict(self)

    def __repr__(self) -> str:  # noqa: D105
        return self.__str__()

    def __str__(self) -> str:  # noqa: D105
        return f"""\
id: {self.id}, \
building: {self.building}, \
floor: {self.floor}, \
location: {self.location}\
"""


class Product(models.Model):
    """
    Product class model for database.

    Each product is defined here.
    Create the product with the name, price and on hand
    Args:
        name (str): The name of the product
        price (float): The price of the product
        on_hand (int): The number of products on hand

    Class Attributes:
        id (int): The id of the product is automatically assigned
        name (str): The name of the product
        price (float): The price of the product
        on_hand (int): The number of products on hand
    """

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    on_hand = models.IntegerField(default=0)

    def as_dict(self) -> dict:
        """
        Return the product as a dictionary.

        Returns:
            dict: The product as a dictionary
        """
        return model_to_dict(self)

    def __repr__(self) -> str:  # noqa: D105
        return self.__str__()

    def __str__(self) -> str:  # noqa: D105
        return f"""\
id: {self.id}, \
name: {self.name}, \
price: {self.price}, \
on_hand: {self.on_hand}\
"""


class Stock(models.Model):
    """
    Stock class model for database.

    Each stock is defined here.
    Create the stock with the vending machine, product and quantity
    Args:
        vending_machine (VendingMachine): The vending machine
        product_info (Product): The product
        quantity (int): The amount of product in the vending machine
    Class Attributes:
        id (int): The id of the stock is automatically assigned
        vending_machine (VendingMachine): The vending machine
        product_info (Product): The product
        quantity (int): The amount of product in the vending machine
    """

    id = models.AutoField(primary_key=True, unique=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    product_info = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def update_quantity(self, quantity: int):
        """
        Update the quantity of the stock.

        Args:
            quantity (int): The amount of product in the vending machine
        """
        self.quantity = quantity
        self.save()

    def as_dict(self) -> dict:
        """
        Return the stock as a dictionary.

        Returns:
            dict: The stock as a dictionary
        """
        vm = self.vending_machine.as_dict()
        product = self.product_info.as_dict()
        return {
            "id": self.id,
            "vending_machine": vm,
            "product_info": product,
            "quantity": self.quantity,
        }

    def __repr__(self) -> str:  # noqa: D105
        return self.__str__()

    def __str__(self) -> str:  # noqa: D105
        return f"""\
id: {self.id}, \
product_info: { {self.product_info} }, \
quantity: {self.quantity}, \
location: { {self.vending_machine} }\
"""
