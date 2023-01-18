from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import *

#------------------------Get things------------------------

def index(request):
    all_stock = Stock.objects.all()
    context = {'all_stock': all_stock}
    return render(request, 'api/index.html', context)


def vendingMachine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    stock = Stock.objects.filter(vending_machine=vm)
    return HttpResponse(stock)

def product(request, product_id):
    return HttpResponse("product")

def stock(request, stock_id):
    return HttpResponse("stock")

#------------------------Add things------------------------

def addVendingMachine(request):
    return HttpResponse("addVendingMachine")

def addProduct(request):
    return HttpResponse("addProduct")

def addStock(request):
    return HttpResponse("addStock")

#------------------------Delete things------------------------

def deleteVendingMachine(request, vending_id):
    return HttpResponse("deleteVendingMachine")

def deleteProduct(request, product_id):
    return HttpResponse("deleteProduct")

def deleteStock(request, stock_id):
    return HttpResponse("deleteStock")

#------------------------Update things------------------------

def updateVendingMachine(request, vending_id):
    return HttpResponse("updateVendingMachine")

def updateProduct(request, product_id):
    return HttpResponse("updateProduct")

def updateStock(request, stock_id):
    return HttpResponse("updateStock")