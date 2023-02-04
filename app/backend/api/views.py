from api.models import Product, Stock, VendingMachine
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

# ------------------------Get/view things------------------------


def get_all_machines(request: HttpRequest) -> HttpResponse:
    """
    Get all the vending machines in the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object.
    Payload:
        machines (list): A list of vending machines.
        for each machine:
            id (int): The id of the vending machine.
            building (str): The building the vending machine is in.
            floor (int): The floor the vending machine is on.
            location (str): The room the vending machine is in.
            stock (list): The stock in the vending machine.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    machines = VendingMachine.objects.all()
    stock_in_machine = []
    for machine in machines:
        stocks = get_stocks_in_machine_as_list(machine)
        stock_in_machine.append(
            {
                "id": machine.id,
                "building": machine.building,
                "floor": machine.floor,
                "location": machine.location,
                "stock": stocks,
            }
        )

    return request_on_content_type(request, "api/all_machines.html", {"machines": stock_in_machine})


def get_machine(request: HttpRequest, vending_id: int) -> HttpResponse:
    """
    Get a specific vending machine based on the id.

    Args:
        request (HttpRequest): The request object.
        vending_id (int): The id of the vending machine.
    Returns:
        HttpResponse: The response object.
    Payload:
        id (int): The id of the vending machine.
        building (str): The building the vending machine is in.
        floor (int): The floor the vending machine is on.
        location (str): The room the vending machine is in.
        stock (list): The stock in the vending machine.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method."}, status=405)
    vm = get_object_or_404(VendingMachine, id=vending_id)
    stock = get_stocks_in_machine_as_list(vm)
    context = {
        "id": vm.id,
        "building": vm.building,
        "floor": vm.floor,
        "location": vm.location,
        "stock": stock,
    }
    return request_on_content_type(request, "api/machine.html", context)


def get_all_products(request: HttpRequest) -> HttpResponse:
    """
    Get all the products in the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object.
    Payload:
        products (list): A list of products.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    products = [product.as_dict() for product in Product.objects.all()]
    return request_on_content_type(request, "api/all_products.html", {"products": products})


def get_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Get a specific product based on the id.

    Args:
        request (HttpRequest): The request object.
        product_id (int): The id of the product.
    Returns:
        HttpResponse: The response object.
    Payload:
        id (int): The id of the product.
        name (str): The name of the product.
        price (float): The price of the product.
        on_hand (int): The number of the product in stock.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    product = get_object_or_404(Product, id=product_id).as_dict()
    context = {"product": product}
    return request_on_content_type(request, "api/product.html", context)


def get_all_stock(request: HttpRequest) -> HttpResponse:
    """
    Get all the stock in the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object.
    Payload:
        stocks (list): A list of stock.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    stock = [stock.as_dict() for stock in Stock.objects.all()]
    return request_on_content_type(request, "api/all_stock.html", {"stocks": stock})


def get_stock(request: HttpRequest, stock_id: int) -> HttpResponse:
    """
    Get a specific stock based on the id.

    Args:
        request (HttpRequest): The request object.
        stock_id (int): The id of the stock.
    Returns:
        HttpResponse: The response object.
    Payload:
        id (int): The id of the stock.
        product (Product): The product in the stock.
        vending_machine (VendingMachine): The vending machine the stock is in.
        quantity (int): The quantity of the stock.
    """
    if request.method != "GET":
        return RESPONSE_CODE_405
    stock = get_object_or_404(Stock, id=stock_id).as_dict()
    return request_on_content_type(request, "api/stock.html", {"stock": stock})


# ------------------------Add things------------------------


def add_vending_machine(request: HttpRequest) -> HttpResponse:
    """
    Add a vending machine to the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object. A Redirect to the Vending Machine page.
    """
    print(repr(request.body))
    print(request.POST)
    print(request.headers)
    if request.method == "GET":
        return request_on_content_type(request, "api/add_vending_machine.html")
    elif request.method == "POST":
        building = request.POST.get("building")
        floor = request.POST.get("floor")
        location = request.POST.get("location")
        new_vm = VendingMachine(building=building, floor=floor, location=location)
        new_vm.save()
        request.method = "GET"
        return get_machine(request, new_vm.id)
    else:
        return RESPONSE_CODE_405


def add_product(request: HttpRequest) -> HttpResponse:
    """
    Add a product to the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object. A Redirect to the Product page.
    """
    if request.method == "GET":
        return request_on_content_type(request, "api/add_product.html")
    elif request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        on_hand = request.POST.get("on_hand")
        new_prod = Product(name=name, price=price, on_hand=on_hand)
        new_prod.save()
        request.method = "GET"
        return get_product(request, new_prod.id)
    else:
        return RESPONSE_CODE_405


def add_stock(request: HttpRequest) -> HttpResponse:
    """
    Add stock to the database.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object. A Redirect to the Stock page.
    """
    if request.method == "GET":
        vm_id = request.GET.get("vending_machine_id", default=1)
        all_vending_machines = VendingMachine.objects.all()
        all_products = Product.objects.all()
        return request_on_content_type(
            request,
            "api/add_stock.html",
            {"default_id": vm_id, "vending_machines": all_vending_machines, "products": all_products},
        )
    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=request.POST.get("vending_machine"))
        prod = get_object_or_404(Product, id=request.POST.get("product"))
        if verify_product_not_in_vending_machine(prod, vm):
            return HttpResponse("Product already in vending machine", status=401)
        quantity = request.POST.get("quantity")
        new_stock = Stock(vending_machine=vm, product_info=prod, quantity=quantity)
        new_stock.save()
        request.method = "GET"
        return get_stock(request, new_stock.id)
    else:
        return RESPONSE_CODE_405


# ------------------------Delete things------------------------


def delete_vending_machine(request: HttpRequest, vending_id: int) -> HttpResponse:
    """
    Delete a vending machine from the database.

    Args:
        request (HttpRequest): The request object.
        vending_id (int): The id of the vending machine.
    Returns:
        HttpResponse: The response object. A Redirect to the Home Page.
    """
    if request.method != "POST":
        return RESPONSE_CODE_405
    vm = get_object_or_404(VendingMachine, id=vending_id)
    vm.delete()
    request.method = "GET"
    return get_all_machines(request)


def delete_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Delete a product from the database.

    Args:
        request (HttpRequest): The request object.
        product_id (int): The id of the product.
    Returns:
        HttpResponse: The response object. A Redirect to the Home Page.
    """
    if request.method != "POST":
        return RESPONSE_CODE_405
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    request.method = "GET"
    return get_all_machines(request)


def delete_stock(request: HttpRequest, stock_id: int) -> HttpResponse:
    """
    Delete stock from the database.

    Args:
        request (HttpRequest): The request object.
        stock_id (int): The id of the stock.
    Returns:
        HttpResponse: The response object. A Redirect to the Home Page.
    """
    if request.method != "POST":
        return RESPONSE_CODE_405
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    request.method = "GET"
    return get_all_machines(request)


# ------------------------Update things------------------------


def update_vending_machine(request: HttpRequest, vending_id: int) -> HttpResponse:
    """
    Update a vending machine in the database.

    If the request is a GET, then the user is being redirected to the update page.
    If the request is a POST, then the user is submitting the update form.
    Form fields that are empty will not be updated.

    Valid Form fields:
        building (str): The building the vending machine is in.
        floor (str): The floor the vending machine is on.
        location (str): The location of the vending machine.
    Args:
        request (HttpRequest): The request object.
        vending_id (int): The id of the vending machine.
    Returns:
        HttpResponse: The response object. A Redirect to the Vending Machine page.
    """
    if request.method == "GET":
        vm = get_object_or_404(VendingMachine, id=vending_id).as_dict()
        return request_on_content_type(request, "api/update_vending_machine.html", vm)

    elif request.method == "POST":
        vm = get_object_or_404(VendingMachine, id=vending_id)
        vm.building = not_null_update_form_field(request.POST.get("building"), vm.building)
        vm.floor = not_null_update_form_field(request.POST.get("floor"), vm.floor)
        vm.location = not_null_update_form_field(request.POST.get("location"), vm.location)
        vm.save()
        request.method = "GET"
        return get_machine(request, vm.id)
    else:
        return RESPONSE_CODE_405


def update_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Update a product in the database.

    If the request is a GET, then the user is being redirected to the update page.
    If the request is a POST, then the user is submitting the update form.
    Form fields that are empty will not be updated.

    Valid Form fields:
        price (str): The price of the product.
        on_hand (str): The quantity of the product on hand.
    Args:
        request (HttpRequest): The request object.
        product_id (int): The id of the product.
    Returns:
        HttpResponse: The response object. A Redirect to the Product page.
    """
    if request.method == "GET":
        prod = get_object_or_404(Product, id=product_id)
        context = {
            "id": prod.id,
            "name": prod.name,
            "price": prod.price,
            "on_hand": prod.on_hand,
        }
        return request_on_content_type(request, "api/update_product.html", context)
    elif request.method == "POST":
        prod = get_object_or_404(Product, id=product_id)
        prod.price = not_null_update_form_field(request.POST.get("price"), prod.price)
        prod.on_hand = not_null_update_form_field(request.POST.get("on_hand"), prod.on_hand)
        prod.save()
        request.method = "GET"
        return get_product(request, prod.id)
    else:
        return RESPONSE_CODE_405


def update_stock(request: HttpRequest, stock_id: int) -> HttpResponse:
    """
    Update stock in the database.

    If the request is a GET, then the user is being redirected to the update page.
    If the request is a POST, then the user is submitting the update form.
    Form fields that are empty will not be updated.

    Valid Form fields:
        quantity (str): The quantity of the product in the vending machine.
    Args:
        request (HttpRequest): The request object.
        stock_id (int): The id of the stock.
    Returns:
        HttpResponse: The response object. A Redirect to the Stock page.
    """
    if request.method == "GET":
        stock = get_object_or_404(Stock, id=stock_id).as_dict()
        return request_on_content_type(request, "api/update_stock.html", stock)
    elif request.method == "POST":
        # only allow updating of quantity here
        stock = get_object_or_404(Stock, id=stock_id)
        stock.quantity = not_null_update_form_field(request.POST.get("quantity"), stock.quantity)
        stock.save()
        request.method = "GET"
        return get_stock(request, stock.id)
    else:
        return RESPONSE_CODE_405


# ------------------------Utility------------------------


def verify_product_not_in_vending_machine(product: Product, vending_machine: VendingMachine) -> bool:
    """
    Verify if the current product is in the vending machine already.

    Args:
        product: Product object
        vending_machine: VendingMachine object
    Returns:
        True if the product IS NOT in the vending machine
        False if the product IS in the vending machine
    """
    return not Stock.objects.filter(product_info=product, vending_machine=vending_machine).exists()


def not_null_update_form_field(form_field: str, model_field: any) -> str:
    """
    Check for an empty form field and updates the model field if not empty.

    Args:
        form_field: the form field to check
        model_field: the model field to update
    Returns:
        the updated model field
    """
    if form_field is not None or form_field != "":
        model_field = form_field
    return model_field


def request_on_content_type(request: HttpRequest, html_template: str, args: dict = {}) -> HttpResponse:
    """
    Return the request object based on the content type.

    Args:
        request: The request object.
        html_template: The html template to render.
        args: The arguments to pass to the request.
    Returns:
        (JsonResponse) if the content type is application/json
        (HttpResponse) if the content type is not application/json
    """
    if request.content_type == "application/json":
        return JsonResponse(args, safe=False)
    else:
        return render(request, html_template, args)


def get_stocks_in_machine_as_list(machine: VendingMachine) -> list[dict]:
    """
    Get the stocks in a vending machine as a list of dictionaries.

    Args:
        machine: The VendingMachine object.
    Returns:
        A list of dictionaries containing the stock information.
    """
    return [stock.as_dict() for stock in Stock.objects.filter(vending_machine=machine)]


RESPONSE_CODE_405 = HttpResponse("Method not allowed", status=405)
