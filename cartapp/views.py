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
    user = request.session.get('email')
    if not user:
        return redirect('login')  # Redirect to login page if user is not authenticated

    user_id = CustomUser.objects.get(email=user)
    print(vars(user_id), 'User Details')
    
    cart_items = MyCart.objects.filter(user_id=user_id.id)
    
    sub_total = 0
    for item in cart_items:
        sub_total += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total
    }
    return render(request, 'userside/cart.html',context)

def proceed(request):
    return render(request,'userside/checkout.html')

def quantity_upadate(request):
    print('loooooooooooooooooooooooooooo')
    if request.method=='POST':
        print(request.POST,"saf")

#         email=request.session['email']
#         customer=CustomUser.objects.get(email=email)
        
#         cart=MyCart.objects.get(user_id=customer.id)
#         cart.quantity=new_quantity
#         cart.save()
#         return render(requestZZZZZZZZZZZZZZZZZZZZZZZZZZZZZz)
            