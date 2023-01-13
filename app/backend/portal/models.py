from django.db import models

# Create your models here.

class VendingMachine(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    building = models.CharField(max_length=50)
    floor = models.IntegerField()
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    def __str__(self):
        return self.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.name