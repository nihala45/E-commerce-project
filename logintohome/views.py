from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from .models import CustomUser
from products.models import newproducts
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.


def signupp(request):
    print("valapraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    if request.method == 'POST':
        username = request.POST['register-username']
        email = request.POST['register-email']
        phone = request.POST['register-phone']
        password = request.POST['register-password']
        confirm_password = request.POST['register-confirm-password']
        print('USERNAMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE',username)
        
        already = CustomUser.objects.filter(email=email)
        if len(phone) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number.")
            return redirect('logintohome:homee')  
        elif password != confirm_password:
            messages.error(request, "Passwords are not same . Please try Again.")
            return redirect('logintohome:homee')  
        elif already:
            messages.error(request, "There is already a Account with this Email")
            return redirect('logintohome:homee')  
        user2 = CustomUser(
            username=username,
            email=email,
            password=password,
            phone=phone,
        )
        user2.save()
        
        
        return redirect('logintohome:otp', id=user2.id)
        

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
                return redirect('logintohome:homee')
            else:
                print("2222222222222222")
                messages.error(request, "Your account is blocked. Please contact support.")
        except CustomUser.DoesNotExist:
            print("3333333333333333")
            messages.error(request, "Incorrect email address or password. Please try again.")
    print("444444444444444")
    return redirect('logintohome:homee')


def homee(request):
    if 'email' in request.session:
        print("9888888888888888888888888888888888899999")
        user = request.session['email']
        return render(request,'userside/home.html',{'user12':user})
    return render(request,'userside/home.html')

def otp(request, id):
    return render(request, 'userside/otpp.html', {'id': id})

def otp_varification(request,id):
    print('hi nihala shirin it is your otp_varification')
    if request.method=='POST':
        user2 = CustomUser.objects.get(id=id)
        p=user2.otp_fld
        print(p,'Hellooooo nihalasss')
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


def shop(request):
    print("jjjjjjjjjjjjjjjjjjjjj")
    products1=newproducts.objects.all()
    print(products1,"99999999999999999999999999999999999999999999999999999999999999999999999999")
    return render(request,'userside/shop.html',{'products':products1})