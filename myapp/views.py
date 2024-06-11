from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.core.files.base import ContentFile
from .models import categories
import base64
import re
from .models import newproducts
from django.views.decorators.cache import never_cache
from .models import CustomUser




@never_cache
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
                print("1111111111111111")
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
    request.session.flush()       
    return redirect('homee')   
@never_cache
def homee(request):
    if 'email' in request.session:
        print("9888888888888888888888888888888888899999")
        user = request.session['email']
        return render(request,'home.html',{'user12':user})
    return render(request,'home.html')
def otp(request, id):
    return render(request, 'otpp.html', {'id': id})


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

    return render(request, "otpp.html")

   
def shop(request):
    print("jjjjjjjjjjjjjjjjjjjjj")
    products1=newproducts.objects.all()
    print(products1,"99999999999999999999999999999999999999999999999999999999999999999999999999")
    return render(request,'shop.html',{'products':products1})





















from django.contrib import messages
@never_cache
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

    return render(request, 'adminlogin.html')

@never_cache
def dashboard(request):
    return render(request,'dashboard.html')
def usermanagement(request):
    user = CustomUser.objects.all()
    return render(request,'users.html',{'user': user})

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
    return render(request, 'category.html', {'items': categoryy})

def addcategory(request):
    return render(request, 'addcategory.html')


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
            return render(request, 'addcategory.html')
        
        
        if categories.objects.filter(category_name=name):
            messages.error(request,'category already exists.please choose a different name.')
            return render(request,'addcategory.html')
            
        category2 = categories(category_name=name)
        category2.save()
        
        return redirect('category')  

    return render(request, 'addcategory.html')

        



def products(request):
    productss=newproducts.objects.all()
    
    return render(request,'products.html',{'products':productss})

def addproduct(request):
    categoryy=categories.objects.all()
    return render(request,'addproduct.html',{'categories':categoryy})

def logout_view(request):
    return redirect('adminlogin')


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

      
    