from django.shortcuts import render, get_object_or_404
from products.models import newproducts

# Create your views here.
def productdetails(request, id):
    product = get_object_or_404(newproducts, id=id)
    return render(request, 'userside/productsdetails.html', {'product': product})