from django.shortcuts import render, get_object_or_404
from products.models import newproducts

def productdetails(request, id):
    product = get_object_or_404(newproducts, id=id)
    return render(request, 'userside/productsdetails.html', {'product': product})
