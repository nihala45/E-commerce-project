from django.shortcuts import render,redirect
from logintohome.models import CustomUser
from django.contrib import messages
from userprofile.models import UserAddress
from userprofile.models import Wallet
from products.models import newproducts
from django.contrib import messages
from django.http import JsonResponse
from cartapp.models import Orders
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone



# Create your views here.



def userdashboard(request):
    
    email = request.session.get('email')
    phone = request.session.get('phone')
    username = request.session.get('username')
    # total_discount_price=get_discounted_price

    context = {
        'username': username,
        'email': email,
        'phone': phone,
    }
    
    user = get_object_or_404(CustomUser, email=email)
    address_queryset = UserAddress.objects.filter(user=user.id)
    ordered_items = Orders.objects.filter(user=user.id).order_by('-id')
    balance=0
    wallet = Wallet.objects.filter(user=user.id)
    for i in wallet:
        balance += i.amount
    addresses = list(address_queryset.values())

    address_context = {
        'addresses': addresses,  
        'ordered_items': ordered_items,
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
    print('NEW USERNAME AND NEW PHONE')
    if request.method == 'POST':
        new_username = request.POST['edit-username']
        new_phone = request.POST['edit-phone']
        user1=request.session.get('email')
        
        obj= CustomUser.objects.get(email=user1)
       
        print(obj.email,".............",obj.username)
        
        obj.username = new_username
        if len(new_phone) == 10 and new_phone.isdigit() and new_phone.count('0') <= 5:
            obj.phone = new_phone
        else:
            print("Invalid phone number:", new_phone)
            messages.error(request, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return redirect('userprofile:editprofile') 
            
        print(new_phone,new_username,'obj_username,obj_phone')
        request.session['username'] = new_username
        request.session['phone'] = new_phone
        obj.save()
        
        return redirect('userprofile:userdashboard')


def add_user_address(request):
    if request.method == 'POST':
        print("hadfsjcmnczxmvdm3456789")
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
        print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg33333 ")
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
    print('hellooooiiiiikooiiiiiiiihelllooooo guyssloooooits nihala shirin')
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
        print(add_id,name,email,phone,address,city,'hiiiiii guyssss')
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
    print("helloo")
    if request.method == 'POST':
        current_password = request.POST.get('current')
        new_password = request.POST.get('password')
        
        user_email = request.session.get('email')
        
        user = CustomUser.objects.get(email=user_email)
        print(user_email,"ggggg",user)
        if(user.password != current_password):
            print("bkdvsnbjkads,bv")
            return JsonResponse({'status': 'wrong', 'message': 'Password is incorrect'})
        else:
            user.password = new_password
            user.save()
            return JsonResponse({'status':'success','message':'Password changed successfully'})
            
        
    #     if user.password != current_password:
    #          messages.error(request, 'This is the incorrect password. Please enter again')
    #     elif new_password != confirm_password:
    #         messages.error(request, 'Confirm password does not match the new password')
    #     elif user.password == current_password and new_password == confirm_password:
           
        
    #    
    #     return redirect('userprofile:userdashboard')
        
def signout(request):
    request.session.flush()
    return redirect('logintohome:homee')

# def order_details(request):
#     user_email=request.session['email']
#     user=CustomUser.objects.get(email=user_email)
#     print(user,'HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIHELPPPP')
#     ordered_items=Orders.objects.get(user_id=user.id)
#     return redirect('userprofile:userdashboard',ordered_items)

def view_details(request, ord_id):
    ordered_item = get_object_or_404(Orders, id=ord_id)
    
    return render(request, "userside/view.html", {'ordered_item': ordered_item})


def cancelOrder(request, or_id):
    user_email = request.session.get('email')
    user = get_object_or_404(CustomUser, email=user_email)
    ord = get_object_or_404(Orders, id=or_id)
    ord.status = "Cancelled"
    ord.save()
    
    if ord.payment_method=='razor_pay':
        wallet_item = Wallet(
        user=user,
        date_time=timezone.now(),
        amount=ord.total_amount_order,
        is_credit=True
        )
        wallet_item.save()

    return redirect(reverse('userprofile:view_details', args=[or_id]))



def returnOrder(request, or_id):
    # user_email = request.session.get('email')
    # user = get_object_or_404(CustomUser, email=user_email)
    ord = get_object_or_404(Orders, id=or_id)
    ord.status = "Return"
    ord.save()

    # wallet_item = Wallet(
    #     user=user,
    #     date_time=timezone.now(),
    #     amount=ord.total_amount_orders,
    #     is_credit=True
    # )
    # wallet_item.save()

    return redirect(reverse('userprofile:view_details', args=[or_id]))





