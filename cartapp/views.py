from django.shortcuts import render,redirect,get_object_or_404
from products.models import newproducts
from logintohome.models import CustomUser
from  cartapp.models import MyCart
# Create your views here.


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')

        # if size not in ['s', 'm', 'l']:
        #     return redirect('product_detail', product_id=product_id)  # Handle invalid size

        user = request.session['email']
        user_id=CustomUser.objects.get(email=user)
        product = get_object_or_404(newproducts, id=product_id)

        
        cart_item, created = MyCart.objects.get_or_create(
            user=user_id,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cartapp:cart_view')

    # return redirect('product_list')

def cart_view(request):
    user = request.session['email']
    user_id=CustomUser.objects.get(email=user)
    print(vars(user_id),'ghajfkitghihihhNIHALAHSIRIRNRRNNRNRNRNRNRNRRNRRRRRRRRRRRRRRRRRRRRRRRRR')
    cart_items = MyCart.objects.filter(user_id=user_id.id)
    
    return render(request, 'userside/cart.html', {'cart_items': cart_items})

def proceed(request):
    return render(request,'userside/checkout.html')