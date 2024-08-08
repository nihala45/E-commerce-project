from django.shortcuts import render,redirect,get_object_or_404
from products.models import newproducts
from logintohome.models import CustomUser
from  newcart.models import MyCart
from django.http import JsonResponse
from userprofile.models import UserAddress
from django.contrib import messages
# Create your views here.
from datetime import date
# from cartapp.models import Orders
from django.contrib.auth.decorators import login_required
from myproject.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
from decimal import Decimal
from couponmanagement.models import Coupon
from couponmanagement.models import CouponUsage
from userprofile.models import Wallet
from django.utils import timezone
from newcart.models import AllOrder
from newcart.models import Ordered_item
from django.views.decorators.cache import never_cache



def add_to_cart(request):
    
    
    if request.method == 'POST':
        user_email = request.session.get('email')
        if not user_email:
            return JsonResponse({'status': 'no user'})
            
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')

        print(f'Product ID: {product_id}, Quantity: {quantity}, Size: {size}')

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
    context={}
    if user_email:
        try:
            user = CustomUser.objects.get(email=user_email)
            cart_items = MyCart.objects.filter(user_id=user.id).order_by('id')
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
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    else:
        messages.warning(request, "Please log in to view your cart.")
        
    return render(request, 'userside/cart.html', context)
    








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
        
            
    
    
    
@never_cache
def proceed_to_checkout(request):
    try:
        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)
        cart_items = MyCart.objects.filter(user_id=user.id)
        wallet = Wallet.objects.filter(user=user.id)
        balance = 0
        
        for i in wallet:
            balance += i.amount
        
        if cart_items.count() == 0:
            return redirect('newcart:show_cart')
        else:
            addresses = UserAddress.objects.filter(user_id=user.id)
            sub_total = 0
            coupon_discount = 0
            dis = False

            for item in cart_items:
                coupon_discount = item.discount_percentage
                if item.product.offer:
                    sub_total += (item.product.price - item.product.offer.discount) * item.quantity
                else:
                    sub_total += item.product.price * item.quantity
            
            discount = (sub_total * coupon_discount) / 100
            final_amount = sub_total - discount
            print(discount, "Discount applied", coupon_discount)

            coupons = Coupon.objects.all()
            applicable_coupons = [coupon for coupon in coupons if sub_total >= coupon.critiria_amount]
            applicable_coupons = [
                coupon for coupon in applicable_coupons
                if not CouponUsage.objects.filter(coupon=coupon, user=user).exists()
            ]
            if final_amount > balance:
                dis = True
            
            if coupon_discount == 0:
                coup=False
            else:
                coup=True
            context = {
                'cart_items': cart_items,
                'sub_total': sub_total,
                'addresses': addresses,
                'coupons': coupons,
                'applicable_coupons': applicable_coupons,
                'discount': discount,
                'final_amount': final_amount,
                'balance_amount': balance,
                'disabled_content': dis,
                'coup':coup
            }
            return render(request, 'userside/checkout.html', context)
    except CustomUser.DoesNotExist:
       
        return redirect('logintohome:homee') 
    except Exception as e:
        print(f"Error occurred: {e}")
        return redirect('newcart:show_cart') 





    
    
    
def apply_coupon(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        user = get_object_or_404(CustomUser, email=user_email)
        coupon_id = request.POST.get('coupon_id')
        
        coupon = get_object_or_404(Coupon, id=coupon_id)
        
       
        current_cart = MyCart.objects.filter(user=user)
        
        
        for item in current_cart:
            item.discount_percentage = coupon.percentage
            item.coupon = coupon 
            item.save() 
        
    
        
        return JsonResponse({'status': 'success', 'message': 'Coupon added successfully.'})

def none_coupon(request):
    print('sooooooooooooooooooooooooooooo')
    user_email = request.session.get('email')

    user = get_object_or_404(CustomUser, email=user_email)
    cart_items = MyCart.objects.filter(user=user)
    for item in cart_items:
        item.discount_percentage = 0  
        item.coupon=None
        item.save()
    
    return JsonResponse({'status':'success'})
        
    




        

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def place_order(request):
    user_email = request.session['email']
    user = CustomUser.objects.get(email=user_email)
    cartItems = MyCart.objects.filter(user_id=user.id)   
    total_price = Decimal(0)
    discount_prg=0
    wallet = Wallet.objects.filter(user=user.id)
    balance=0
    for i in wallet:
        balance += i.amount
    
    for item in cartItems:
            discount_prg=item.discount_percentage
            if item.product.offer:
                total_price += (item.product.price - item.product.offer.discount)*(item.quantity)
            else:
                total_price += item.product.price * item.quantity
    discount = (total_price*discount_prg)/100
    total_price =total_price-discount
    
    
    if request.method == 'POST':
        address_id = request.POST.get('selectedAddress')
        payment_method = request.POST.get('selectedPaymentMethod')
        ordered_date = date.today()
        address = UserAddress.objects.get(id=address_id)
        if payment_method == 'cash_on_delivery':
    
            total_order = AllOrder(
                user=user,
                order_date=ordered_date,
                payment_method=payment_method,
                total_amount=total_price,
                discount_amount=discount,
            )
            total_order.save()  
        
            for item in cartItems:
                Ordered_item.objects.create(
                    order=total_order, 
                    address=address,
                    status='placed',
                    product=item.product,
                    product_qty=item.quantity,
                    product_size=item.size,
                )         

            
            if cartItems and cartItems[0].coupon:
                coupon_use = CouponUsage(
                    user=user,
                    coupon=cartItems[0].coupon
                )
                coupon_use.save()
                
            

            
           
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
        else:
            total_order = AllOrder(
                user=user,
                order_date=ordered_date,
                payment_method=payment_method,
                total_amount=total_price,
                discount_amount=discount,
            )
            total_order.save()  
        
            for item in cartItems:
                Ordered_item.objects.create(
                    order=total_order, 
                    address=address,
                    status='placed',
                    product=item.product,
                    product_qty=item.quantity,
                    product_size=item.size,
                )         

            
            if cartItems and cartItems[0].coupon:
                coupon_use = CouponUsage(
                    user=user,
                    coupon=cartItems[0].coupon
                )
                coupon_use.save()
                
            wallet_item = Wallet(
            user=user,
            date_time=timezone.now(),
            amount=-total_price,
            is_credit=False,
            )
            wallet_item.save()

            
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
            
            
def razor_save(request):
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
    if request.method == 'POST':
        address_id = request.POST.get('selectedAddress')
        payment_method = request.POST.get('selectedPaymentMethod')
        ordered_date = date.today()
        address = UserAddress.objects.get(id=address_id)

        total_order = AllOrder(
            user=user,
            order_date=ordered_date,
            payment_method=payment_method,
            total_amount=total_price,
            discount_amount=discount,
        )
        total_order.save()  
        
    for item in cartItems:
        Ordered_item.objects.create(
            order=total_order, 
            address=address,
            status='placed',
            product=item.product,
            product_qty=item.quantity,
            product_size=item.size,
        )         

            
    if cartItems and cartItems[0].coupon:
        coupon_use = CouponUsage(
        user=user,
        coupon=cartItems[0].coupon
        )
        coupon_use.save()
    

            
        
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


from django.db import transaction


def failurepage(request):
    user_email = request.session.get('email')
    user = get_object_or_404(CustomUser, email=user_email)
    
    cartItems = MyCart.objects.filter(user=user)
    
    total_price = Decimal(0)
    discount_prg = 0
    
    for item in cartItems:
        discount_prg = item.discount_percentage
        if item.product.offer:
            total_price += (item.product.price - item.product.offer.discount) * item.quantity
        else:
            total_price += item.product.price * item.quantity
    
    discount = (total_price * discount_prg) / 100
    total_price -= discount
    

    amount = Decimal(request.GET.get('amount', 0))
    address_id = request.GET.get('address')
    address = get_object_or_404(UserAddress, id=address_id)
    
   
    ordered_date = date.today()
    total_order = AllOrder(
        user=user,
        order_date=ordered_date,
        payment_method='razor_pay',
        total_amount=amount,
        discount_amount=discount,
    )
    total_order.save()
    
   
    for item in cartItems:
        Ordered_item.objects.create(
            order=total_order,
            address=address,
            status='Pending',
            product=item.product,
            product_qty=item.quantity,
            product_size=item.size,
        )
        
     
        pro = newproducts.objects.get(id=item.product_id)
        if item.size == 's':
            pro.small = int(pro.small) - item.quantity
        elif item.size == 'm':
            pro.medium = int(pro.medium) - item.quantity
        else:
            pro.large = int(pro.large) - item.quantity
        pro.save()
    
   
    if cartItems and cartItems[0].coupon:
        CouponUsage.objects.create(
            user=user,
            coupon=cartItems[0].coupon
        )
    
   
    cartItems.delete()
    
    return render(request, 'userside/failurepage.html', {'amount': amount})

def continue_shopping(request):
    return redirect('logintohome:shop')


    
    

    
    
def Remove_cart_product(request,it_id):
    cart_product = MyCart.objects.get(id=it_id)
    cart_product.delete()
    return redirect('newcart:show_cart')


def successpage(request):
    return render(request,'userside/success.html')