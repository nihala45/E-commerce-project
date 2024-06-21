from django.shortcuts import render

# Create your views here.


def cartp(request):
    return render(request,'userside/cart.html')

def proceed(request):
    return render(request,'userside/checkout.html')