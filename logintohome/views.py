from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from .models import CustomUser
from products.models import newproducts
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from category.models import categories
from django.http import JsonResponse
from django.urls import reverse
from wishlist.models import WishlistProduct
from django.db.models import Q
import pyotp
from django.core.mail import send_mail



# Create your views here.

def homee(request):
    if 'email' in request.session:
        
        user = request.session['email']
        return render(request,'userside/home.html',{'user12':user})
    return render(request,'userside/home.html')

def Signup(request):
    
    if request.method == 'POST':
        username = request.POST['user_username']
        email = request.POST['user_email']
        phone = request.POST['user_phone']
        password = request.POST['user_password']
        confirm_password = request.POST['user_confirm']
        
        already = CustomUser.objects.filter(email=email) 
        
        if already:
            return JsonResponse({'status':'already','message':'There is already a Account with this Email'})   
        else:
            user2 = CustomUser(
                username=username,
                email=email,
                password=password,
                phone=phone,
            )
            user2.save()
        
        
        redirect_url = reverse('logintohome:otp', args=[user2.id])
        return JsonResponse({'status':'success','redirect_url': redirect_url})   
        
       

def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('user_email')
        password = request.POST.get('user_password')
        try:
            user = CustomUser.objects.get(email=email, password=password)
            if user and not user.is_blocked:
                
                request.session['email']=email
                request.session['phone'] = user.phone 
                request.session['username'] = user.username
                return JsonResponse({'status':'success'})
                
               

                
            else:
                return JsonResponse({'status':'block','message':'Your account is blocked. Please contact support.'})
                
                
        except CustomUser.DoesNotExist:
            return JsonResponse({'status':'wrong','message':'Incorrect email address or password. Please try again.'})


    return redirect('logintohome:homee')



def otp(request, id):
    return render(request, 'userside/otpp.html', {'id': id})

def otp_varification(request,id):
    if request.method=='POST':
        user2 = CustomUser.objects.get(id=id)
        p=user2.otp_fld
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
            return redirect('logintohome:homee')
        

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("logintohome:otp", id=id)

    return render(request, "userside/otpp.html")






def filterProduct(request):
    category1 = categories.objects.all()
    products=newproducts.objects.none()
        
    if request.method =='POST':
        selected_categories=request.POST.getlist('categories')
        for i in selected_categories:
            pro=newproducts.objects.filter(category_id=i)
            products=products.union(pro)
            
    
            
    elif request.method =='GET':
        s=''
        s=request.GET.get('sortby')
        if s:
            if s == 'Low_to_High':
                price_low_high = newproducts.objects.all().order_by('price')
                products=products.union(price_low_high)
            elif s=='High_to_Low':
                price_high_low=newproducts.objects.all().order_by('-price')
                products=products.union(price_high_low)
            elif s=='a_to_z':
                product_az=newproducts.objects.all().order_by('name')
                products=products.union(product_az)
            elif s=='z_to_a':
                product_za=newproducts.objects.all().order_by('-name')
                products=products.union(product_za)
            elif s=='new_arrival':
                products_new = newproducts.objects.all().order_by('-id')[:2]
                
                products=products.union(products_new)
                
            
        else:
            search_item=request.GET.get('q')
            search_pro=newproducts.objects.filter(name__icontains=search_item)
            products=products.union(search_pro)
        

        
        
    else:
        products_all= newproducts.objects.all() 
        products=products.union(products_all)
    return render(request, 'userside/shop.html', {'products': products, 'category': category1})



def shop_to_home(request):
    return redirect('logintohome:homee')


def shop(request):
    
    user_email = request.session.get('email')
    products = newproducts.objects.all().order_by('-id')
    category1 = categories.objects.all()
    wish = []
    user=False
    
    
    if user_email:
        try:
            user =True
            user_eamil=request.session.get('email')
            user=CustomUser.objects.get(email=user_eamil)
            category1 = categories.objects.all()
            products = newproducts.objects.all().order_by('-id')
            
            wishlist_items = WishlistProduct.objects.filter(user_id=user)
            wish=[]
            for i in wishlist_items:
                wish.append(i.product.id)
        except:
            pass
    

    return render(request, 'userside/shop.html', {'products': products, 'category': category1,'wish_item':wish ,'user_eamil':user})





def resend_otp(request):
    if request.method == "POST":
        user_id = request.POST.get('userid')

        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                
               
                secret_key = pyotp.random_base32()
                otp = pyotp.TOTP(secret_key)
                otp_code = otp.now()

                
                user.otp_secret = secret_key
                user.otp_fld = otp_code
                user.save()
                subject="OTP Varification"
                message=f"Your OTP for verification is:{otp_code}"
                from_email="nihalashirin02@gmail.com"
                send_mail(subject,message,from_email,[user.email])

                
                return redirect(reverse('logintohome:otp', args=[user.id]))

            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'User ID not provided.')
    
    return redirect('logintohome:default_page')
