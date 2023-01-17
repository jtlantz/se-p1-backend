from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import *

def index(request):
    all_stock = Stock.objects.all()
    context = {'all_stock': all_stock}
    return render(request, 'api/index.html', context)

def vendingMachine(request, vending_id):
    vm = get_object_or_404(VendingMachine, id=vending_id)
    stock = Stock.objects.filter(vending_machine=vm)
    return HttpResponse(stock)