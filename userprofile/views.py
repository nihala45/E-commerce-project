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
    # all_address=UserAddress.objects.get(address_Email=email)
    # if all_address:
    #     address_context = {
    #         'all_address': all_address,
    #         'address_name': all_address.address_name,
    #         'address_Phone': all_address.address_Phone,
    #         'Address': all_address.Address,
    #         'landmark': all_address.landmark,
    #         'city': all_address.city,
    #         'district': all_address.district,
    #         'state': all_address.state,
    #         'pin': all_address.pin,
    #     }
    #     context.update(address_context)
    
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


# def save_address(request):
#     if request.method == 'POST':
#         address_name = request.POST['address-username']
#         address_Email = request.POST['address-email']
#         address_Phone = request.POST['address-phone']
#         Address = request.POST['detaild-address']
#         landmark = request.POST['address-landmark']
#         city = request.POST['address-city']
#         district = request.POST['address-district']
#         state = request.POST['address-state']
#         pin = request.POST['address-pin']
        
        
#         user_address = UserAddress(
#             address_name=address_name,
#             address_Email=address_Email,
#             address_Phone=address_Phone,
#             Address=Address,
#             landmark=landmark,
#             city=city,
#             district=district,
#             state=state,
#             pin=pin
#         )
#         user_address.save()
#         print(address_name)

#         return redirect('userprofile:userdashboard')
    

def signout(request):
    request.session.flush()
    return redirect('logintohome:homee')