from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

from api.models import VendingMachine, Product, Stock


# ------------------------Get/view things------------------------


def get_all_machines(request):
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
    return render(request, 'api/all_machines.html', {"machines": stock_in_machine})


def get_machine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    stock = Stock.objects.filter(vending_machine=vm)
    context = {
        "id": vm.id,
        "building": vm.building,
        "floor": vm.floor,
        "location": vm.location,
        "stock": stock,
    }
    return render(request, 'api/machine.html', context)


def get_all_products(request):
    products = Product.objects.all()
    return render(request, 'api/all_products.html', {"products": products})


def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {"product": product}
    # TODO: Find locations where this stock is at and display it as well
    context["locations"] = {}
    return render(request, 'api/product.html', context)


def get_all_stock(request):
    stock = Stock.objects.all()
    return render(request, 'api/all_stock.html', {"stocks": stock})


def get_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    context = {"stock": {
        "id": stock.id,
        "product": stock.product_info,
        "vending_machine": stock.vending_machine,
        "quantity": stock.quantity,
    }}
    return render(request, 'api/stock.html', context)


# ------------------------Add things------------------------


def add_vending_machine(request):
    if request.method == "GET":
        return render(request, 'api/add_vending_machine.html')
    elif request.method == "POST":
        building = request.POST.get("building")
        floor = request.POST.get("floor")
        location = request.POST.get("location")

        new_vm = VendingMachine(building=building, floor=floor, location=location)
        new_vm.save()
        return get_machine(request, new_vm.id)
    else:
        # return a 405 error
        return HttpResponse("Method not allowed", status=405)


def add_product(request):
    if request.method == "GET":
        return render(request, 'api/add_product.html')
    elif request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        on_hand = request.POST.get("on_hand")
        new_prod = Product(name=name, price=price, on_hand=on_hand)
        new_prod.save()
        return get_product(request, new_prod.id)
    else:
        return HttpResponse("Method not allowed", status=405)


def add_stock(request):
    if request.method == "GET":
        vm_id = request.GET.get("vending_machine_id", default=1)
        all_vending_machines = VendingMachine.objects.all()
        all_products = Product.objects.all()
        return render(request, 'api/add_stock.html',
                      {"default_id": vm_id,
                       "vending_machines": all_vending_machines,
                       "products": all_products
                       })
    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=request.POST.get("vending_machine"))
        prod = get_object_or_404(Product, id=request.POST.get("product"))
        if not verify_product_not_in_vending_machine(prod, vm):
            return HttpResponse("Product already in vending machine", status=400)
        quantity = request.POST.get("quantity")
        new_stock = Stock(vending_machine=vm, product_info=prod, quantity=quantity)
        new_stock.save()
        return get_stock(request, new_stock.id)
    else:
        return HttpResponse("Method not allowed", status=405)


# ------------------------Delete things------------------------


def delete_vending_machine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    vm.delete()
    return get_all_machines(request)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return get_all_machines(request)


def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    return get_all_machines(request)


# ------------------------Update things------------------------


def update_vending_machine(request, vending_id):
    # send form data to edit the vending machine
    if request.method == "GET":
        vm = get_object_or_404(VendingMachine, id=vending_id)
        context = {
            "id": vm.id,
            "building": vm.building,
            "floor": vm.floor,
            "location": vm.location,
        }
        return render(request, 'api/update_vending_machine.html', context)

    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=vending_id)
        vm.building = not_null_update_form_field(request.POST.get("building"), vm.building)
        vm.floor = not_null_update_form_field(request.POST.get("floor"), vm.floor)
        vm.location = not_null_update_form_field(request.POST.get("location"), vm.location)
        vm.save()
        return get_machine(request, vm.id)
    else:
        return HttpResponse("Method not allowed", status=405)


def update_product(request, product_id):
    if request.method == "GET":
        prod = get_object_or_404(Product, id=product_id)
        context = {
            "id": prod.id,
            "name": prod.name,
            "price": prod.price,
            "on_hand": prod.on_hand,
        }
        return render(request, 'api/update_product.html', context)
    elif request.method == "POST":
        prod = get_object_or_404(Product, id=product_id)
        prod.price = not_null_update_form_field(request.POST.get("price"), prod.price)
        prod.on_hand = not_null_update_form_field(request.POST.get("on_hand"), prod.on_hand)
        prod.save()
        return get_product(request, prod.id)
    else:
        return HttpResponse("Method not allowed", status=405)


def update_stock(request, stock_id):
    if request.method == "GET":
        stock = get_object_or_404(Stock, id=stock_id)
        vm = stock.vending_machine
        prod = stock.product_info
        context = {
            "id": stock.id,
            "building": vm.building,
            "floor": vm.floor,
            "location": vm.location,
            "product": prod.name,
            "quantity": stock.quantity,
        }
        return render(request, 'api/update_stock.html', context)
    elif request.method == "POST":
        # only allow updating of quantity here
        stock = get_object_or_404(Stock, id=stock_id)
        stock.quantity = not_null_update_form_field(request.POST.get("quantity"), stock.quantity)
        stock.save()
        return get_stock(request, stock.id)
    else:
        return HttpResponse("Method not allowed", status=405)


# ------------------------Utility------------------------


def verify_product_not_in_vending_machine(product: Product, vending_machine: VendingMachine) -> bool:
    """
    Verifies if the current product is in the vending machine already
    args:
        product: Product object
        vending_machine: VendingMachine object
    returns:
        True if the product IS NOT in the vending machine
        False if the product IS in the vending machine
    """
    return not Stock.objects.filter(product_info=product, vending_machine=vending_machine).exists()


def not_null_update_form_field(form_field, model_field):
    """
    Checks for an empty form field and updates the model field if not empty
    or returns the original value if it is empty
    args:
        form_field: the form field to check
        model_field: the model field to update
    returns:
        the updated model field
    """
    if form_field is not None or form_field != '':
        model_field = form_field
    return model_field
