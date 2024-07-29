from django.shortcuts import render
from products.models import newproducts
from django.shortcuts import render, get_object_or_404, redirect
from wishlist.models import WishlistProduct
from logintohome.models import CustomUser
# Create your views here.

def Wishlist(request):
    wishlist_items=WishlistProduct.objects.all().order_by('id')
    return render(request,'userside/wishlist.html',{'wishlist_item':wishlist_items})

def add_to_wishlist(request, prod_id):
    email = request.session.get('email')
    user = get_object_or_404(CustomUser, email=email)
    wishlist_item = WishlistProduct.objects.filter(user=user, product_id=prod_id).first()
    
    if wishlist_item:
        wishlist_item.delete()
    else: 
        WishlistProduct.objects.create(user=user, product_id=prod_id)
    
    return redirect('logintohome:shop')

def add_to_cart(request):
    email = request.session.get('email')
    user = get_object_or_404(CustomUser, email=email)
    
    
def remove_from_wishlist(request, wishlist_id):
    try:
        print('Attempting to remove item from wishlist...', wishlist_id)

        user_email = request.session.get('email')
        if not user_email:
            return redirect('wishlist:login')  

        user = CustomUser.objects.get(email=user_email)
        print('User ID:', user.id)
        
        product = WishlistProduct.objects.filter(id=wishlist_id, user_id=user.id).first()
        
        if product:
            product.delete()
            print('Product removed from wishlist.')
        else:
            print('Product not found in wishlist.')
        
    except CustomUser.DoesNotExist:
        print('User does not exist.')
        return redirect('wishlist:login') 

    except WishlistProduct.DoesNotExist:
        print('Wishlist product does not exist.')
        return redirect('wishlist:view_wishlist')  
    
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return redirect('wishlist:view_wishlist')  
    return redirect('wishlist:Wishlist')  