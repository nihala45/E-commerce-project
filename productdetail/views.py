from django.shortcuts import render, get_object_or_404
from products.models import newproducts
from category.models import categories
from wishlist.models import WishlistProduct
from userprofile.models import CustomUser
from django.http import JsonResponse

def productdetails(request, id):
    user_email=request.session.get('email')
    product = get_object_or_404(newproducts, id=id)
    category=categories.objects.get(id=product.category.id)
    wishlist_item=[]
    try:
        user_email=request.session.get('email')
        product = get_object_or_404(newproducts, id=id)
        category=categories.objects.get(id=product.category.id)
        wishlist_item=WishlistProduct.objects.get(product_id=product.id)
    except:
        pass
    
       

    return render(request, 'userside/productsdetails.html', {'product': product,'categoryy':category,'user_email':user_email,'wishlist_item':wishlist_item})

def addToWishlist(request):
    email = request.session.get('email')
    user = get_object_or_404(CustomUser, email=email)
    if request.method=="POST":
        prod_id=request.POST.get('prod_id')
    wishlist_item = WishlistProduct.objects.filter(user=user, product_id=prod_id).first()
    if wishlist_item:
        wishlist_item.delete()
        return JsonResponse({'status':'deleted'})
    else: 
        WishlistProduct.objects.create(user=user, product_id=prod_id)
        return JsonResponse({'status':'added'})
