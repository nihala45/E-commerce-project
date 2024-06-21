from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
#from .models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.core.files.base import ContentFile
from .models import categories
#from .models import UserAddress
# from .models import varients
import base64
import re
#from .models import newproducts

#from .models import CustomUser
from django.contrib.auth.decorators import login_required



# USER SIDE




def loginn(request):
   
    if request.method == 'POST':
        email = request.POST.get('singin-email')
        password = request.POST.get('singin-password')
        print(email,"9999999999999999999999")
        try:
            user = CustomUser.objects.get(email=email, password=password)
            print(user,"88888888888888888")
            if user and not user.is_blocked:
                request.session['email']=email
                request.session['phone'] = user.phone 
                request.session['username'] = user.username
                print("Session variables set successfully:", request.session.items())
                return redirect('homee')
            else:
                print("2222222222222222")
                messages.error(request, "Your account is blocked. Please contact support.")
        except CustomUser.DoesNotExist:
            print("3333333333333333")
            messages.error(request, "Incorrect email address or password. Please try again.")
    print("444444444444444")
    return redirect('homee')



def userlogout(request):
         
    return redirect('homee')   

def homee(request):
    if 'email' in request.session:
        print("9888888888888888888888888888888888899999")
        user = request.session['email']
        return render(request,'userside/home.html',{'user12':user})
    return render(request,'userside/home.html')
def otp(request, id):
    return render(request, 'userside/otpp.html', {'id': id})


def signupp(request):
    print("valapraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    if request.method == 'POST':
        username = request.POST['register-username']
        email = request.POST['register-email']
        phone = request.POST['register-phone']
        password = request.POST['register-password']
        confirm_password = request.POST['register-confirm-password']
        
        already = CustomUser.objects.filter(email=email)
        if len(phone) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number.")
            return redirect('homee')  # Assuming 'signup' is the name of your sign-up page URL
        elif password != confirm_password:
            messages.error(request, "Passwords are not same . Please try Again.")
            return redirect('homee')  # Assuming 'signup' is the name of your sign-up page URL
        elif already:
            messages.error(request, "There is already a Account with this Email")
            return redirect('homee')  # Assuming 'signup' is the name of your sign-up page URL
        user2 = CustomUser(
            username=username,
            email=email,
            password=password,
            phone=phone,
        )
        user2.save()
        
        
        return redirect('otp', id=user2.id)

def otp_varification(request,id):
    print('hi nihala shirin it is your otp_varification')
    if request.method=='POST':
        user2 = CustomUser.objects.get(id=id)
        p=user2.otp_fld
        print(p,'phjgfytgdgfhjp')
        entered_otp=request.POST.get("otp")
        p=int(p)
        entered_otp=int(entered_otp)
        if entered_otp == p:
            user2 = CustomUser.objects.get(id=id)
            user2.is_verified = True
            user2.save()
            messages.success(
                request, "Email verified successfully. You can now log in."
            )
            return redirect('homee')
        

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otp", id=id)

    return render(request, "userside/otpp.html")

   
def shop(request):
    print("jjjjjjjjjjjjjjjjjjjjj")
    products1=newproducts.objects.all()
    print(products1,"99999999999999999999999999999999999999999999999999999999999999999999999999")
    return render(request,'userside/shop.html',{'products':products1})

def userdashboard(request):
    
    email = request.session.get('email')
    phone = request.session.get('phone')
    username = request.session.get('username')
    

    context = {
        'username': username,
        'email': email,
        'phone': phone,
    }
    all_address=UserAddress.objects.get(address_Email=email)
    if all_address:
        address_context = {
            'all_address': all_address,
            'address_name': all_address.address_name,
            'address_Phone': all_address.address_Phone,
            'Address': all_address.Address,
            'landmark': all_address.landmark,
            'city': all_address.city,
            'district': all_address.district,
            'state': all_address.state,
            'pin': all_address.pin,
        }
        context.update(address_context)
    jjj="nihala"
    print("Session variables retrieved in userdashboard view:", email, phone, username,"ttttttttttttttttttttttttttttttttttttt",all_address,all_address.landmark)
    return render(request, 'userside/userdashboard.html',context)



    




def signout(request):
    request.session.flush()
    return redirect('homee')
    






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
            return redirect('editprofile') 
            
        print(new_phone,new_username,'obj_username,obj_phone')
        request.session['username'] = new_username
        request.session['phone'] = new_phone
        
        return redirect('userdashboard')


    
           
def save_address(request):
    if request.method == 'POST':
        address_name = request.POST['address-username']
        address_Email = request.POST['address-email']
        address_Phone = request.POST['address-phone']
        Address = request.POST['detaild-address']
        landmark = request.POST['address-landmark']
        city = request.POST['address-city']
        district = request.POST['address-district']
        state = request.POST['address-state']
        pin = request.POST['address-pin']
        
        
        user_address = UserAddress(
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
        user_address.save()
        print(address_name)

        return redirect('userdashboard')

def productdetails(request):
    return render(request,'userside/productsdetails.html')
    
    
# def save_address(request):





def cartp(request):
    return render(request,'userside/cart.html')


def checkout(request):
    return render(request,'userside/checkout.html')


def proceed(request):
    return render(request,'userside/checkout.html')




# ADMIN SIDE  



def adminloginn(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                
                error_message = "You are not authorized to access the admin dashboard."
                messages.error(request, error_message)
        else:
            
            error_message = "Incorrect username or password. Please try again."
            messages.error(request, error_message)

    return render(request, 'customadmin/adminlogin.html')


def dashboard(request):
    return render(request,'customadmin/dashboard.html')
def usermanagement(request):
    user = CustomUser.objects.all()
    return render(request,'customadmin/users.html',{'user': user})

def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('usermanagement')  

def unblock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('usermanagement')  

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
import re
from .models import categories

def categorymanagement(request):
    categoryy = categories.objects.all()
    return render(request, 'customadmin/category.html', {'items': categoryy})

def addcategory(request):
    return render(request, 'customadmin/addcategory.html')


# def edit_category(request, category_id):
#     category =categories.objects.get(id=category_id)
#     # Handle edit logic here, e.g., update category name
#     if request.method == 'POST':
#         new_category_name = request.POST.get('new_category_name')
#         category.category_name = new_category_name
#         category.save()
#         return redirect('category') 
#     return render(request, 'edit.html', {'category': category})

# def delete_category(request, category_id):
#     category = categories.objects.get(id=category_id)
    
#     category.delete()
#     return redirect('category')  



def savecategory(request):
    if request.method == 'POST':
        name = request.POST['category']
        
        
        if not re.match("^[A-Za-z][A-Za-z]*$", name):
            
            messages.error(request, 'Category name must start with a letter and contain only letters without numbers or leading spaces.')
            return render(request, 'customadmin/addcategory.html')
        
        
        if categories.objects.filter(category_name=name):
            messages.error(request,'category already exists.please choose a different name.')
            return render(request,'customadmin/addcategory.html')
            
        category2 = categories(category_name=name)
        category2.save()
        
        return redirect('category')  

    return render(request, 'customadmin/addcategory.html')

        



def products(request):
    productss=newproducts.objects.all()
    
    return render(request,'customadmin/products.html',{'products':productss})

def addproduct(request):
    categoryy=categories.objects.all()
    return render(request,'customadmin/addproduct.html',{'categories':categoryy})

def logout_view(request):
    return redirect('customadmin/adminlogin')


def saveproducts(request):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )
    if request.method=='POST':
        name=request.POST['productname']
        category_id = request.POST['productcategory']
        description=request.POST['productdescription']
        price=request.POST['productprice']
        if not re.match("^[A-Za-z]+$", name):
            messages.error(request, "Product name should only contain letters without spaces or numbers.")
            return redirect('addproduct') 
        category = categories.objects.get(id=category_id)

        if "croppedImageData" in request.POST:
            img1 = request.POST["croppedImageData"]

            
            if img1:
                format, imgstr = img1.split(";base64,")
                ext = re.search(r"/(.*?)$", format).group(1)

               
                decoded_file = base64.b64decode(imgstr)
                img_file = ContentFile(decoded_file, name=f"cropped_image.{ext}")
        img7 = request.FILES["img1"] if "img1" in request.FILES else None
                
        img2 = request.FILES["img2"] if "img2" in request.FILES else None
        img3 = request.FILES["img3"] if "img3" in request.FILES else None
        img4 = request.FILES["img4"] if "img4" in request.FILES else None 
        print(category,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        products2=newproducts(
           name=name,
           category=category,
           description=description,
           price=price,
           image1=img7,
           image2=img2,
           image3=img3,
           image4=img4,
           
        )    
        products2.save()
        return redirect('products')

      
def addvarient(request):
    print('ADD VARIENT FUNCTION IS WORKING')
    # if request.method == 'POST':
    #     q1 = request.POST['smallQuantity']
    #     q2 = request.POST['mediumQuantity']
    #     q3 = request.POST['largeQuantity']
    #     print(q1,q2,q3)
    #     already=newproducts.objects.get(product_id=prod_id)
    #     if already:
    #         already.small=q1
    #         already.medium=q2
    #         already.large=q2
    #         already.save()
    print(prod_id)
        
        
        
    return redirect('myapp:products')

# def varientreport(request):
#     report=varients.objects.all()
#     return render(request,'customadmin/products.html',{'report':report})
    