from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import authenticate,login


# Create your views here.
def adminloginn(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('adminside:dashboard')
            else:
                
                error_message = "You are not authorized to access the admin dashboard."
                messages.error(request, error_message)
        else:
            
            error_message = "Incorrect username or password. Please try again."
            messages.error(request, error_message)

    return render(request, 'customadmin/adminlogin.html')


def dashboard(request):
    return render(request,'customadmin/dashboard.html')

def logout_view(request):
    return redirect('customadmin/adminlogin')