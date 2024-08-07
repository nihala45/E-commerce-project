from django.shortcuts import render, get_object_or_404
from products.models import newproducts
from category.models import categories

def productdetails(request, id):
    product = get_object_or_404(newproducts, id=id)
    category=categories.objects.get(id=product.category.id)
    return render(request, 'userside/productsdetails.html', {'product': product,'categoryy':category})
