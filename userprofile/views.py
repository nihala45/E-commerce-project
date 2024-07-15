from django.shortcuts import render,redirect
from logintohome.models import CustomUser
from django.contrib import messages
from userprofile.models import UserAddress
from products.models import newproducts
from django.contrib import messages
from django.http import JsonResponse
from cartapp.models import Orders
from django.shortcuts import render, get_object_or_404
from django.urls import reverse



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
    print(user.id,'helllllllllllloooooooooooooooooooooooo')
    address = UserAddress.objects.filter(user=user.id)
        
    ordered_items = Orders.objects.filter(user=user.id).order_by('-id')
    
    address_context = {
        'addresses': address,
        'ordered_items': ordered_items
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
        address_name = request.POST.get('Email')
        address_Email = request.POST.get('name')
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
    
    
def remove_address(request,address_id):
    address1=UserAddress.objects.get(id=address_id)
    address1.delete()
    return redirect('userprofile:userdashboard')    
    
def edit_address(request,address_id):
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    address2=UserAddress.objects.get(id=address_id)
    print(address2,'LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
    return render(request,'userside/userdashboard.html',address2)


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
def cancelOrder(request,or_id):
    ord=Orders.objects.get(id=or_id)
    ord.status="Cancelled"
    ord.save()
    return redirect(reverse('userprofile:view_details', args=[or_id]))
    