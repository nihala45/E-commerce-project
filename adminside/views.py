from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
def adminloginn(request):
    if 'is_superuser' in request.session:
        super_user = request.session['is_superuser']
        return render(request, 'customadmin/dashboard.html', {'super': super_user})
    
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            request.session['is_superuser'] = True
            return redirect('adminside:dashboard')
        else:
            error_message = "Incorrect username or password. Please try again."
            messages.error(request, error_message)
    
    return render(request, 'customadmin/adminlogin.html')

    

@never_cache
@login_required(login_url='adminside:adminlogin')
def dashboard(request):
    return render(request,'customadmin/dashboard.html')

def logout_view(request):
    if request.session.get('is_superuser'):
        del request.session['is_superuser']  
    logout(request)  
    return redirect('adminside:adminlogin')