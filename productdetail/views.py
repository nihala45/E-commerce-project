from django.shortcuts import render, get_object_or_404
from products.models import newproducts
from category.models import categories
def productdetails(request, id):
    print('is is product detail pageee')
    product = get_object_or_404(newproducts, id=id)
    category=categories.objects.get(id=product.category.id)
    print(category,'cateforyyyy')
    return render(request, 'userside/productsdetails.html', {'product': product,'categoryy':category})
