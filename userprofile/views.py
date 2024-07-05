from django.shortcuts import render,redirect
from logintohome.models import CustomUser
from django.contrib import messages
from userprofile.models import UserAddress
from products.models import newproducts




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
    print(vars(m),'HELLLOOOOOOOOOOOO')
    address=UserAddress.objects.filter(user=m)
    print(vars(address),'HIIIIIIIIIIIII')
    address_context = {
            'addresses': address
        }
    context.update(address_context)
    
    # print("Session variables retrieved in userdashboard view:", email, phone, username,"ttttttttttttttttttttttttttttttttttttt",all_address,all_address.landmark)
    
    return render(request, 'userside/userdashboard.html',context)



    
def editprofile(request):
    username=request.session.get('username')
    phone=request.session.get('phone')
    m={
        'username':username,
        'phone':phone,
        
    }
    print("Session variables retrieved in EDIT PROFILE:",  phone, username)
    return render(request, 'userside/editprofile.html', m)

def save_edit(request):
    print('NEW USERNAME AND NEW PHONE')
    if request.method == 'POST':
        new_username = request.POST['edit-username']
        new_phone = request.POST['edit-phone']
        user1=request.session.get('email')
        
        obj= CustomUser.objects.get(email=user1)
        print(obj,"iiiii")
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
        
        return redirect('userprofile:userdashboard')


def add_user_address(request):
    print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
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
    print(vars(User_Address),'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
    
def remove_address(request,address_id):
    address1=UserAddress.objects.get(id=address_id)
    address1.delete()
    return redirect('userprofile:userdashboard')    
    
    
def signout(request):
    request.session.flush()
    return redirect('logintohome:homee')