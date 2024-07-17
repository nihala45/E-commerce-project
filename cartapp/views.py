from django.shortcuts import render,redirect,get_object_or_404
from products.models import newproducts
from logintohome.models import CustomUser
from  cartapp.models import MyCart
from django.http import JsonResponse
from userprofile.models import UserAddress
from django.contrib import messages
# Create your views here.
from datetime import date
from cartapp.models import Orders
from django.contrib.auth.decorators import login_required


# 
def add_to_cart(request):
    print('helllooo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')

        print(f'Product ID: {product_id}, Quantity: {quantity}, Size: {size}')

        user_email = request.session['email']
        user = CustomUser.objects.get(email=user_email)
        product = get_object_or_404(newproducts, id=product_id)

        print("User and product fetched successfully.")

        try:
            cart_item = MyCart.objects.get(user=user, product=product, size=size)
            print(f'Existing cart item: {cart_item}')
            return JsonResponse({'status': 'already'})
        except MyCart.DoesNotExist:
            MyCart.objects.create(user=user, product=product, size=size, quantity=quantity)
            print('New cart item created.')
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid request'}, status=400)


def cart_view(request):
    user = request.session.get('email')
    if not user:
        return redirect('login') 

    user_id = CustomUser.objects.get(email=user)
    print(vars(user_id), 'User Details')
    
    cart_items = MyCart.objects.filter(user_id=user_id.id).order_by('product_id')
    
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
    user_email=request.session['email']
    user_id=CustomUser.objects.get(email=user_email)
    if request.method=='POST':
        print(request.POST,"saf")
        prod_id=request.POST.get('product_id') 
        count = int(request.POST.get('count'))
        prduct_size=request.POST.get('size')
    products=newproducts.objects.get(id=prod_id)
    product_quantity=0
    if prduct_size == 's':
         product_quantity=int(products.small)
    elif prduct_size =='m':
         product_quantity=int(products.medium)
    else:
         product_quantity=int(products.large)
         
    print(product_quantity,"gdghfahjnbwd")
    
        

    cart_product=MyCart.objects.get(user_id=user_id.id,product_id=prod_id,size=prduct_size)
    if count==1:
        
        if (cart_product.quantity + count) > product_quantity:
            print("out of stock")
            return JsonResponse({'status':'out'})
        else:
            print("increasing")
            cart_product.quantity+=count 
            cart_product.save()
            return JsonResponse({'status':'success'})
    else:
        if cart_product.quantity==1:
            return JsonResponse({'status':'zero'})   
        else:
            cart_product.quantity+=count
            cart_product.save()
            return JsonResponse({'status':'success'})
        
            
    
    
    


def proceed_to_checkout(request): 
    user_email = request.session.get('email')
    user = CustomUser.objects.get(email=user_email)
    cart_items = MyCart.objects.filter(user_id=user.id)
    if cart_items.count() == 0:
        return redirect('cartapp:show_cart')
    else:
        addresses = UserAddress.objects.filter(user_id=user.id)
        sub_total = 0
        for item in cart_items:
            sub_total += item.product.price * item.quantity
    
        context = {
            'cart_items': cart_items,
            'sub_total': sub_total,
            'addresses':addresses
        }
        return render(request, 'userside/checkout.html', context)
        


def place_order(request):
    user_email = request.session['email']
    user = CustomUser.objects.get(email=user_email)
    cartItems=MyCart.objects.filter(user_id=user.id)   
    
    if request.method=='POST':
        address_id=request.POST.get('selected_address')
        payment_method=request.POST.get('payment_method')
        ordered_date = date.today()
        cart_items = MyCart.objects.filter(user_id=user.id)
        address=UserAddress.objects.get(id=address_id)
        
        for item in cart_items:
            print(address_id,item.product.id,item.quantity,"kkkkk",)
            order_detail=Orders(
                user=user,
                address=address,
                ordered_date=ordered_date,
                payment_method=payment_method,
                product=item.product,
                status='Placed',
                product_qty=item.quantity,
                product_price=item.product.price * item.quantity,
                product_size=item.size
                ).save()
            pro = newproducts.objects.get(id=item.product_id)
            if item.size == 's':
                pro.small = int(pro.small) - item.quantity
            elif item.size == 'm':
                pro.medium = int(pro.medium) - item.quantity
            else:
                pro.large = int(pro.large) - item.quantity
            
            pro.save()
                
                
                
                
                
                
            
            print(order_detail,"hiii")
        
        cart_items.delete()
    return render(request,'userside/success.html')

    


        

def continue_shopping(request):
    return redirect('logintohome:shop')


    
    
def show_cart(request):
    user_email = request.session.get('email')
    if user_email:
        user = CustomUser.objects.get(email=user_email)
        cart_items = MyCart.objects.filter(user_id=user.id).order_by('product_id')
        sub_total = 0
        for item in cart_items:
            sub_total += item.product.price * item.quantity
        context = {
            'cart_items': cart_items,
            'sub_total': sub_total
        }
        return render(request, 'userside/cart.html', context)
    
    
def Remove_cart_product(request,it_id):
    cart_product = MyCart.objects.get(id=it_id)
    cart_product.delete()
    return redirect('cartapp:show_cart')