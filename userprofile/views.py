from django.shortcuts import render,redirect
from logintohome.models import CustomUser
from django.contrib import messages
from userprofile.models import UserAddress
from userprofile.models import Wallet
from newcart.models import AllOrder
from newcart.models import Ordered_item
from products.models import newproducts
from django.contrib import messages
from django.http import JsonResponse
# from cartapp.models import Orders
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from myproject.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
from django.utils import timezone

# Create your views here.



def userdashboard(request):
    
    email = request.session.get('email')
    phone = request.session.get('phone')
    username = request.session.get('username')
    context = {
        'username': username,
        'email': email,
        'phone': phone,
    }
    
    user = get_object_or_404(CustomUser, email=email)
    address_queryset = UserAddress.objects.filter(user=user.id).order_by('id')
    ordered_items=AllOrder.objects.filter(user=user.id).order_by('id')

    balance=0
    wallet = Wallet.objects.filter(user=user.id)
    for i in wallet:
        balance += i.amount
    addresses = list(address_queryset.values())

    address_context = {
        'ordered_item':ordered_items,
        'addresses': addresses,  
        'wallet_items':wallet,
        'balance':balance
    }
    context.update(address_context)
    
    
    
    return render(request, 'userside/userdashboard.html', context)

    



        





    
def editprofile(request):
    username=request.session.get('username')
    phone=request.session.get('phone')
    m={
        'username':username,
        'phone':phone,
        
    }
    return render(request, 'userside/editprofile.html', m)


def save_edit(request):
    if request.method == 'POST':
        new_username = request.POST['edit-username']
        new_phone = request.POST['edit-phone']
        user1=request.session.get('email')
        
        obj= CustomUser.objects.get(email=user1)
       
       
        
        obj.username = new_username
        if len(new_phone) == 10 and new_phone.isdigit() and new_phone.count('0') <= 5:
            obj.phone = new_phone
        else:
            messages.error(request, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return redirect('userprofile:editprofile') 
            
        
        request.session['username'] = new_username
        request.session['phone'] = new_phone
        obj.save()
        
        return redirect('userprofile:userdashboard')


def add_user_address(request):
    if request.method == 'POST':
        address_name = request.POST.get('name')
        address_Email = request.POST.get('Email')
        address_Phone = request.POST.get('phone')
        Address = request.POST.get('Address')
        landmark = request.POST.get('Landmark')
        city = request.POST.get('city')
        district = request.POST.get('District')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        user_Email=request.session['email']
        user=CustomUser.objects.get(email=user_Email)
        User_Address = UserAddress.objects.create(
            user=user,  
            address_name=address_name,
            address_Email=address_Email,
            address_Phone=address_Phone,
            Address=Address,
            landmark=landmark,
            city=city,
            district=district,
            state=state,
            pin=pin
        )
        User_Address.save()
        return JsonResponse({'status':'success'})

def edit_address(request):
    if request.method == "POST":
        add_id = request.POST.get('address_id')
        name = request.POST.get('edit_name')
        email = request.POST.get('edit_email')
        phone = request.POST.get('edit_phone')
        address = request.POST.get('edit_address')
        city = request.POST.get('edit_city')
        district = request.POST.get('edit_district')
        state = request.POST.get('edit_state')
        pin = request.POST.get('edit_pincode')
        address_obj = get_object_or_404(UserAddress, id=add_id)

        address_obj.address_name = name
        address_obj.address_Email = email
        address_obj.address_Phone = phone
        address_obj.Address = address
        address_obj.city = city
        address_obj.district = district
        address_obj.state = state
        address_obj.pin = pin

        address_obj.save()

        return JsonResponse({'status': 'success'})
    
    
    
def remove_address(request,address_id):
    address1=UserAddress.objects.get(id=address_id)
    address1.delete()
    return redirect('userprofile:userdashboard')    
    


def change_password(request):
   
    if request.method == 'POST':
        current_password = request.POST.get('current')
        new_password = request.POST.get('password')
        
        user_email = request.session.get('email')
        
        user = CustomUser.objects.get(email=user_email)
        
        if(user.password != current_password):
            return JsonResponse({'status': 'wrong', 'message': 'Password is incorrect'})
        else:
            user.password = new_password
            user.save()
            return JsonResponse({'status':'success','message':'Password changed successfully'})
            
    
        
def signout(request):
    request.session.flush()
    return redirect('logintohome:homee')


def view_details(request, ord_id):
    
    ordered_items = Ordered_item.objects.filter(order_id=ord_id)
    order_status=True
    for i in ordered_items:
        if i.status=='Pending':
            order_status=False
            break
    all_order = AllOrder.objects.get(id=ord_id)
    unit_prices=[]
    total_amounts=[]
    total_product_quantity = 0
    first_address = ordered_items.first().address if ordered_items.exists() else None

    
    for item in ordered_items:
        total_product_quantity += item.product_qty
    
    
    total_items = len(ordered_items)
    discount_price = Decimal(all_order.discount_amount) / Decimal(total_product_quantity) if total_product_quantity > 0 else Decimal(0)
   
    
    
    total_qty=0
    for item in ordered_items:
        
        if item.product.offer:
        
            amount = Decimal(item.product.price) - Decimal(item.product.offer.discount)
            
        else:
            
            
            amount = Decimal(item.product.price)
            
        
        
        unit_price = amount - discount_price
        unit_prices.append(unit_price)
        
        total_amount = unit_price * Decimal(item.product_qty)
        total_amounts.append(total_amount)
        
        
    
    

    return render(request, "userside/orderview.html", {'all_orders':all_order,'ordered_item':ordered_items,'unit_price':unit_prices,'total_amounts':total_amounts,'first_addressess': first_address,'order_status':order_status})




def cancelApproval(request):
    if request.method == 'POST':
        ord_id = request.POST.get('ord_id')
        response = request.POST.get('response')
        
        order_item = Ordered_item.objects.get(id=ord_id)
        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)
        
        if response == 'approve':
            ord = get_object_or_404(Ordered_item, id=ord_id)
            ord.status = "Cancelled"
            ord.save()
            
            
            if ord.product_size == 's':
                ord.product.small = str(int(ord.product.small) + ord.product_qty)
            elif ord.product_size == 'm':
                ord.product.medium = str(int(ord.product.medium) + ord.product_qty)
            elif ord.product_size == 'l':
                ord.product.large = str(int(ord.product.large) + ord.product_qty)
            ord.product.save()
            
            main_order = AllOrder.objects.get(id=ord.order_id)
            items = Ordered_item.objects.filter(order_id=main_order)
            product_quantity = sum(item.product_qty for item in items)
            discount_price = Decimal(main_order.discount_amount) / Decimal(product_quantity) if product_quantity > 0 else Decimal(0)
            
            if ord.product.offer:
                amount = Decimal(ord.product.price) - Decimal(ord.product.offer.discount)
            else:
                amount = Decimal(ord.product.price)
            
            last_price = (amount - discount_price) * Decimal(ord.product_qty)
            
            
            if main_order.payment_method == 'razor_pay':
         
                result=Wallet.objects.create(
                    user=user,
                    date_time=timezone.now(),
                    amount=last_price,
                    is_credit=True
                )
                
            return JsonResponse({'cancel': True})
        
        else:  
            ord = get_object_or_404(Ordered_item, id=ord_id)
            
            ord.status = "placed" 
            ord.save()
            
            
            
            return JsonResponse({'cancel': False, 'notcancel': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



def returnApproval(request):
    if request.method == 'POST':
        ord_id = request.POST.get('ord_id')
        response = request.POST.get('response')
        
        order_item = Ordered_item.objects.get(id=ord_id)
        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)
        
        if response == 'approve':
            ord = get_object_or_404(Ordered_item, id=ord_id)
            ord.status = "Returned"
            ord.save()
            
            # Adjust inventory based on product size
            if ord.product_size == 's':
                ord.product.small = str(int(ord.product.small) + ord.product_qty)
            elif ord.product_size == 'm':
                ord.product.medium = str(int(ord.product.medium) + ord.product_qty)
            elif ord.product_size == 'l':
                ord.product.large = str(int(ord.product.large) + ord.product_qty)
            ord.product.save()
            
            main_order = AllOrder.objects.get(id=ord.order_id)
            items = Ordered_item.objects.filter(order_id=main_order)
            product_quantity = sum(item.product_qty for item in items)
            discount_price = Decimal(main_order.discount_amount) / Decimal(product_quantity) if product_quantity > 0 else Decimal(0)
            
            if ord.product.offer:
                amount = Decimal(ord.product.price) - Decimal(ord.product.offer.discount)
            else:
                amount = Decimal(ord.product.price)
            
            last_price = (amount - discount_price) * Decimal(ord.product_qty)
            
           
            if main_order.payment_method == 'razor_pay':
                result=Wallet.objects.create(
                    user=user,
                    date_time=timezone.now(),
                    amount=last_price,
                    is_credit=True
                )
               
            
            return JsonResponse({'return': 'success'})
        
        else:  
            ord = get_object_or_404(Ordered_item, id=ord_id)
            
            ord.status = "Delivered"  
            ord.save()
            
            
            
            return JsonResponse({'cancel': False, 'notcancel': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def cancelOrder(request):
    if request.method == 'POST':
        
        user_email = request.session.get('email')
        ord_id = request.POST.get('orderId')
        reason = request.POST.get('cancelReason')
        
        
        user = get_object_or_404(CustomUser, email=user_email)
        
        ord = get_object_or_404(Ordered_item, id=ord_id)

        ord.status = "CancelRequest"
        
        ord.cancel_reason=reason
        ord.save()
        
        
            
        
        return JsonResponse({'cancel': True})
    






def returnOrder(request):
    user_email = request.session.get('email')
    ord_id = request.POST.get('orderId')
    reason = request.POST.get('returnReason')
        
    user = get_object_or_404(CustomUser, email=user_email)
        
    ord = get_object_or_404(Ordered_item, id=ord_id)

    ord.status = "ReturnRequested"
    ord.return_reason=reason
    ord.save()
        
     
    
        
    return JsonResponse({'cancel': True})
    




def download_product_invoice(request, order_id):
    try:
        order = AllOrder.objects.get(id=order_id)
        items=Ordered_item.objects.filter(order_id=order)
        first_address = items.first().address if items.exists() else None
        unit_prices=[]
        total_amounts=[]
        total_product_quantity=0
        for item in items:
            total_product_quantity += item.product_qty
        discount_price = Decimal(order.discount_amount) / Decimal(total_product_quantity) if total_product_quantity > 0 else Decimal(0)
        for item in items:
        
            if item.product.offer:
        
                amount = Decimal(item.product.price) - Decimal(item.product.offer.discount)
            
            else:
                amount = Decimal(item.product.price)
            unit_price = amount - discount_price
            unit_prices.append(unit_price)
        
            total_amount = unit_price * Decimal(item.product_qty)
            total_amounts.append(total_amount)
            
        
    except AllOrder.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    context = {
    "all_orders": order,
    "ordered_item": items,
    "first_addressess": first_address,
    "unit_price": unit_prices,
    "total_amounts": total_amounts,
    }
    template = get_template("userside/invoice.html")
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if pdf:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="invoice_{order_id}.pdf"'
        )
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)
    
    
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
def razorPaypayment(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId')
      

        
        order=AllOrder.objects.get(id=orderId)
        amount=order.total_amount
        DATA = {
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": '1',
            "receipt": "receipt_1"
        }
        payment_order = client.order.create(data=DATA)
        return JsonResponse({
            'status': 'razorpay',
            'payment_order': payment_order,
            'key': RAZORPAY_KEY_ID,
            'order_id':orderId
        })


def razorStatusUpdate(request):
    if request.method == "POST":   
        order_Id = request.POST.get('order_id')
        
    deliverd_items=Ordered_item.objects.filter(order_id=order_Id)
    for item in deliverd_items:
        item.status = 'placed'
        item.save()
    return JsonResponse({"status":'success'})