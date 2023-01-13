from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("main page for portal")

def second_page(request):
    return HttpResponse("If you can read this you are on the second page")
