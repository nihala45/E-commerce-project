from django.shortcuts import render,redirect,get_object_or_404
from logintohome.models import CustomUser
from django.contrib import messages
from django.core.files.base import ContentFile
from category.models import categories
from userprofile.models import UserAddress
from products.models import newproducts
from logintohome.models import CustomUser
from django.contrib.auth.decorators import login_required




# Create your views here.
# @login_required(login_url='adminside:adminlogin')
def usermanagement(request):
    user = CustomUser.objects.all().order_by('-id')
    return render(request,'customadmin/users.html',{'user': user})

@login_required(login_url='adminside:adminlogin')
def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('usermanagement:usermanagement')  

@login_required(login_url='adminside:adminlogin')
def unblock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('usermanagement:usermanagement')  

