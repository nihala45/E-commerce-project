from django.shortcuts import render,redirect,get_object_or_404
from logintohome.models import CustomUser
from django.contrib import messages
from django.core.files.base import ContentFile
from category.models import categories
from userprofile.models import UserAddress
from products.models import newproducts
from logintohome.models import CustomUser




# Create your views here.
def usermanagement(request):
    user = CustomUser.objects.all()
    return render(request,'customadmin/users.html',{'user': user})

def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('usermanagement:usermanagement')  

def unblock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('usermanagement:usermanagement')  