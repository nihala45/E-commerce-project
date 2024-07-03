from django.shortcuts import render
from products.models import newproducts
# Create your views here.


def cart(request,product_id):
    pro=newproducts.object.get(id=product_id)
    return render(request,'userside/cart.html',{'prod':pro})

def proceed(request):
    return render(request,'userside/checkout.html')