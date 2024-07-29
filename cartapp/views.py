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
from myproject.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
from decimal import Decimal
from couponmanagement.models import Coupon
from couponmanagement.models import CouponUsage






def add_to_cart(request):
    
    
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
    



def show_cart(request):
    user_email = request.session.get('email')
    if user_email:
        user = CustomUser.objects.get(email=user_email)
        cart_items = MyCart.objects.filter(user_id=user.id).order_by('product_id')
        sub_total = 0
        
        for item in cart_items:
            if item.product.offer:
                sub_total += (item.product.price - item.product.offer.discount)*(item.quantity)
            else:
                sub_total+= item.product.price * item.quantity
        context = {
            'cart_items': cart_items,
            'sub_total': sub_total,
        }
        return render(request, 'userside/cart.html', context)
    




# def proceed(request):
#     return render(request,'userside/checkout.html')



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
        coupon_discount=0
        m=0
        
        for item in cart_items:
            coupon_discount=item.discount_percentage
            if item.product.offer:
                sub_total += (item.product.price - item.product.offer.discount)*(item.quantity)
            else:
                sub_total+= item.product.price * item.quantity
       
        discount = (sub_total*coupon_discount)/100
        final_amount =sub_total-discount
        print(discount,"fffffffffffffffffffffffffffffffffffffffffff",coupon_discount)
        
        coupons = Coupon.objects.all()
        applicable_coupons = [coupon for coupon in coupons if sub_total >= coupon.critiria_amount]
        
    
        context = {
            'cart_items': cart_items,
            'sub_total': sub_total,
            'addresses':addresses,
            'coupons': coupons,
            'applicable_coupons': applicable_coupons,
            'discount':discount,
            'final_amount':final_amount
        }
        return render(request, 'userside/checkout.html', context)
    

# 



    
    
    
def apply_coupon(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        user = get_object_or_404(CustomUser, email=user_email)
        coupon_id = request.POST.get('coupon_id')


        coupon = get_object_or_404(Coupon, id=coupon_id)
        # if CouponUsage.objects.filter(coupon=coupon, user=user).exists():
        #     return JsonResponse({'status': 'already'})
        current_cart=MyCart.objects.filter(user_id=user.id)
        print(current_cart,"hhhhhhhhhhhhhhhhhhhhhhhh")
        for item in current_cart:
            item.discount_percentage = coupon.percentage
            item.save()  
        print("jjjjjjjj")
        CouponUsage.objects.create(coupon=coupon, user=user)
        return JsonResponse({'status': 'success', 'message': 'Coupon added successfully.'})
    
        
    




        

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def place_order(request):
    user_email = request.session['email']
    user = CustomUser.objects.get(email=user_email)
    cartItems = MyCart.objects.filter(user_id=user.id)   
    total_price = Decimal(0)
    discount_prg=0
    for item in cartItems:
            discount_prg=item.discount_percentage
            if item.product.offer:
                total_price += (item.product.price - item.product.offer.discount)*(item.quantity)
            else:
                total_price += item.product.price * item.quantity
    discount = (total_price*discount_prg)/100
    total_price =total_price-discount
    print(discount_prg,total_price,discount,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                
    
    if request.method == 'POST':
        address_id = request.POST.get('selectedAddress')
        payment_method = request.POST.get('selectedPaymentMethod')
        ordered_date = date.today()
        address = UserAddress.objects.get(id=address_id)
        if payment_method == 'cash_on_delivery':
            for item in cartItems:
                Orders(
                    user=user,
                    address=address,
                    ordered_date=ordered_date,
                    payment_method=payment_method,
                    product=item.product,
                    product_qty=item.quantity,
                    discount_amt=discount,
                    product_price=item.product.price * item.quantity,
                    product_size=item.size,
                    status='placed'
                ).save()
            
            pro = newproducts.objects.get(id=item.product_id)
            if item.size == 's':
                pro.small = int(pro.small) - item.quantity
            elif item.size == 'm':
                pro.medium = int(pro.medium) - item.quantity
            else:
                pro.large = int(pro.large) - item.quantity
            
            pro.save()
            
        
            cartItems.delete()
            return JsonResponse({'status': 'success'})   
        elif payment_method == 'razor_pay':
            total_price_float = float(total_price)
            DATA = {
                "amount": int(total_price_float * 100),
                "currency": "INR",
                "payment_capture": '1',
                "receipt": "receipt_1"
            }
            payment_order = client.order.create(data=DATA)
            return JsonResponse({
                'status': 'razorpay',
                'payment_order': payment_order,
                'key': RAZORPAY_KEY_ID
            })
            
def razor_save(request):
    user_email = request.session['email']
    user = CustomUser.objects.get(email=user_email)
    cartItems = MyCart.objects.filter(user_id=user.id)  
    discount_prg=cartItems[0].discount_percentage
    if request.method == 'POST':
        address_id = request.POST.get('selectedAddress')
        payment_method = request.POST.get('selectedPaymentMethod')
        ordered_date = date.today()
        address = UserAddress.objects.get(id=address_id)
    for item in cartItems:
            Orders(
                user=user,
                address=address,
                ordered_date=ordered_date,
                payment_method=payment_method,
                product=item.product,
                discount_amt=discount_prg,
                product_qty=item.quantity,
                product_price=item.product.price * item.quantity,
                product_size=item.size,
                status='placed' 
            ).save()
            
            pro = newproducts.objects.get(id=item.product_id)
            if item.size == 's':
                pro.small = int(pro.small) - item.quantity
            elif item.size == 'm':
                pro.medium = int(pro.medium) - item.quantity
            else:
                pro.large = int(pro.large) - item.quantity
            
            pro.save()
        
            cartItems.delete()
            return JsonResponse({'status': 'success'}) 

# def place_order(request):
#     user_email = request.session['email']
#     user = CustomUser.objects.get(email=user_email)
#     cartItems = MyCart.objects.filter(user_id=user.id)   
#     total_price = Decimal(0)
    
#     if request.method == 'POST':
#         address_id = request.POST.get('selectedAddress')
#         payment_method = request.POST.get('selectedPaymentMethod')
#         ordered_date = date.today()
#         address = UserAddress.objects.get(id=address_id)
        
#         for item in cartItems:
#             Orders(
#                 user=user,
#                 address=address,
#                 ordered_date=ordered_date,
#                 payment_method=payment_method,
#                 product=item.product,
#                 product_qty=item.quantity,
#                 product_price=item.product.price * item.quantity,
#                 product_size=item.size,
#                 status='placed' if payment_method == 'cash_on_delivery' else 'pending'
#             ).save()
            
#             pro = newproducts.objects.get(id=item.product_id)
#             if item.size == 's':
#                 pro.small = int(pro.small) - item.quantity
#             elif item.size == 'm':
#                 pro.medium = int(pro.medium) - item.quantity
#             else:
#                 pro.large = int(pro.large) - item.quantity
            
#             pro.save()
#             total_price += item.product.price * item.quantity
        
#         cartItems.delete()
        
#         if payment_method == 'cash_on_delivery':
#             return JsonResponse({'status': 'success'})    
#         elif payment_method == 'razor_pay':
#             total_price_float = float(total_price)
#             DATA = {
#                 "amount": int(total_price_float * 100),  # Amount in paise
#                 "currency": "INR",
#                 "payment_capture": '1',
#                 "receipt": "receipt_1"
#             }
#             payment_order = client.order.create(data=DATA)
#             return JsonResponse({
#                 'status': 'razorpay',
#                 'payment_order': payment_order,
#                 'key': RAZORPAY_KEY_ID
#             })               
                
                
            
            
        
       

    


        

def continue_shopping(request):
    return redirect('logintohome:shop')


    
    

    
    
def Remove_cart_product(request,it_id):
    cart_product = MyCart.objects.get(id=it_id)
    cart_product.delete()
    return redirect('cartapp:show_cart')


def successpage(request):
    return render(request,'userside/success.html')