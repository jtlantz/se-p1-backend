from django.db import models

"""
Each vending machine has a unique ID to identify the vending machine, this is auto generated
More information associated with the vending machine but the required info is listed below
More information may be added later on
"""
class VendingMachine(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    building = models.CharField(max_length=50)
    floor = models.IntegerField()
    location = models.CharField(max_length=50)

"""
Each product, e.g. Snickers, Aquarius, etc... is defined here.
This is indented to indicate the product that we have on hand in total
The stock here DOES NOT mean we have this stock in a certain vending machine
This is just a list of on-hand stock
"""
class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()

"""
The stock is a association between the vending machine and the product
The current stock on hand inside the vending machine is in this table
"""
class Stock(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    #The vending machine that this stock is associated with
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    #the name of the product can be inherited from the product table
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #How much stock is currently in the vending machine
    quantity = models.IntegerField()