from django.db import models

class VendingMachine(models.Model):
    """
    Each vending machine has a unique ID to identify the vending machine, this is auto generated
    More information associated with the vending machine but the required info is listed below
    More information may be added later on
    """
    id = models.AutoField(primary_key=True, unique=True)
    building = models.CharField(max_length=50)
    floor = models.IntegerField()
    location = models.CharField(max_length=50)

    def __repr__(self) -> dict:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
        id: {self.id}, building: {self.building}, floor: {self.floor}, location: {self.location}
        """


class Product(models.Model):
    """
    Each product, e.g. Snickers, Aquarius, etc... is defined here.
    This is indented to indicate the product that we have on hand in total
    The stock(on_hand) here DOES NOT mean we have this stock in a certain vending machine
    This is just a list of on-hand stock
    """
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    on_hand = models.IntegerField(default=0)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
        id: {self.id}, name: {self.name}, price: {self.price}, on_hand: {self.on_hand}
        """


class Stock(models.Model):
    """
    The stock is an association between the vending machine and the product
    The current stock on hand inside the vending machine is in this table
    """
    id = models.AutoField(primary_key=True, unique=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    product_info = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def update_quantity(self, quantity: int):
        self.quantity = quantity
        self.save()

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"""
        id: {self.id}, product_info: { {self.product_info} }, quantity: {self.quantity}, location: { {self.vending_machine} }
        """
