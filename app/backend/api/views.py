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
        "building": vm.building,
        "floor": vm.floor,
        "location": vm.location,
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
        building = request.POST.get("building")
        floor = request.POST.get("floor")
        location = request.POST.get("location")

        new_vm = VendingMachine(building=building, floor=floor, location=location)
        new_vm.save()
        return vendingMachine(request, new_vm.id)
    else:
        #return a 405 error
        return HttpResponse("Method not allowed", status=405)

def addProduct(request):
    if request.method == "GET":
        return render(request, 'api/addProduct.html')
    elif request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        on_hand = request.POST.get("on_hand")
        new_prod = Product(name=name, price=price, on_hand=on_hand)
        new_prod.save()
        return product(request, new_prod.id)
    else:
        return HttpResponse("Method not allowed", status=405)

def addStock(request):
    if request.method == "GET":
        vm_id = 1
        if request.GET.get("vending_machine_id") != None:
            vm_id = request.GET.get("vending_machine_id")
        all_vending_machines = VendingMachine.objects.all()
        all_products = Product.objects.all()
        return render(request, 'api/addStock.html', {"default_id": vm_id, 
        "vending_machines": all_vending_machines, 
        "products": all_products
        })
    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=request.POST.get("vending_machine"))
        prod = get_object_or_404(Product, id=request.POST.get("product"))
        if not verifyProductNotInVendingMachine(prod, vm):
            return HttpResponse("Product already in vending machine", status=400)
        quantity = request.POST.get("quantity")
        new_stock = Stock(vending_machine=vm, product_info=prod, quantity=quantity)
        new_stock.save()
        return stock(request, new_stock.id)
    else:
        return HttpResponse("Method not allowed", status=405)

#------------------------Delete things------------------------

def deleteVendingMachine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    vm.delete()
    return index(request)

def deleteProduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return index(request)

def deleteStock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    return index(request)

#------------------------Update things------------------------
def notNullUpdateFormField(form_field, model_field):
    if form_field != None or form_field != '':
        model_field = form_field
    return model_field

def updateVendingMachine(request, vending_id):
    #send form data to edit the vending machine
    if request.method=="GET":
        vm = get_object_or_404(VendingMachine, id=vending_id)
        context = {
            "id": vm.id,
            "building": vm.building,
            "floor": vm.floor,
            "location": vm.location,
        }
        return render(request, 'api/updateVendingMachine.html', context)

    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=vending_id)
        vm.building = notNullUpdateFormField(request.POST.get("building"), vm.building)
        vm.floor = notNullUpdateFormField(request.POST.get("floor"), vm.floor)
        vm.location = notNullUpdateFormField(request.POST.get("location"), vm.location)
        vm.save()
        return vendingMachine(request, vm.id)
    else:
        return HttpResponse("MEthod not allowed", status=405)

def updateProduct(request, product_id):
    return HttpResponse("updateProduct")

def updateStock(request, stock_id):
    return HttpResponse("updateStock")

#------------------------Utility------------------------
"""
Verifies if the current product is in the vending machine already
args:
    product: Product object
    vending_machine: VendingMachine object
returns:
    True if the product IS NOT in the vending machine
    False if the product IS in the vending machine
"""
def verifyProductNotInVendingMachine(product:Product, vending_machine:VendingMachine)->bool:
    if Stock.objects.filter(product_info=product, vending_machine=vending_machine).exists():
        return False
    return True