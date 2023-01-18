from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import *

#------------------------Get/view things------------------------

def index(request):
    machines = VendingMachine.objects.all()
    stock_in_machine = [
        {
            "id": machine.id,
            "building": machine.building,
            "floor": machine.floor,
            "location": machine.location, 
            "stock": Stock.objects.filter(vending_machine=machine)
        }
        for machine in machines
        ]
    return render(request, 'api/index.html', {"machines": stock_in_machine})


def vendingMachine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    stock = Stock.objects.filter(vending_machine=vm)
    context = {
        "id": vm.id,
        "stock": stock,
    }
    return render(request, 'api/vendingMachine.html', context)

def allProducts(request):
    products = Product.objects.all()
    return render(request, 'api/allProducts.html', {"products": products})

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {"product": product}
    #TODO: Find locations where this stock is at and display it as well
    context["locations"] = {}
    return render(request, 'api/product.html', context)

def allStock(request):
    stock = Stock.objects.all()
    return render(request, 'api/allStock.html', {"stocks": stock})

def stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    context = {"stock" : {
        "id": stock.id,
        "product": stock.product_info,
        "vending_machine": stock.vending_machine,
        "quantity": stock.quantity,
    }}
    return render(request, 'api/stock.html', context)

#------------------------Add things------------------------

def addVendingMachine(request):
    if request.method == "GET":
        return render(request, 'api/addVendingMachine.html')
    elif request.method == "POST":
        ...
    else:
        #return a 405 error
        return HttpResponse("Method not allowed", status=405)
        
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