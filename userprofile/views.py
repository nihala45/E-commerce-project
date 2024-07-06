from django.shortcuts import render,redirect
from logintohome.models import CustomUser
from django.contrib import messages
from userprofile.models import UserAddress
from products.models import newproducts
from django.contrib import messages
from django.http import JsonResponse



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
    
    m=CustomUser.objects.get(email=email)
    address=UserAddress.objects.filter(user=m)
    address_context = {
            'addresses': address
        }
    context.update(address_context)
    
    
    
    return render(request, 'userside/userdashboard.html',context)



    
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
        if len(new_phone) == 10 and new_phone.isdigit():
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
        address_name = request.POST.get('address-username')
        address_Email = request.POST.get('address-email')
        address_Phone = request.POST.get('address-phone')
        Address = request.POST.get('detaild-address')
        landmark = request.POST.get('address-landmark')
        city = request.POST.get('address-city')
        district = request.POST.get('address-district')
        state = request.POST.get('address-state')
        pin = request.POST.get('address-pin')
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
        return redirect('userprofile:userdashboard')
    
    
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
            return JsonResponse({'status': 'wrong', 'message': 'Password is incorrect  maandaaa'})
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