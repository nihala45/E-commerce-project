from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from category.models import categories
import re
from products.models import newproducts
from django.contrib.auth.decorators import login_required
from logintohome.models import CustomUser 
from django.core.serializers import serialize
from django.http import JsonResponse

@login_required(login_url='adminside:adminlogin')
def categorymanagement(request):
    category = categories.objects.all()
    categories_json = serialize('json', category) 
    categories_list = list(category.values())    
    return render(request, 'customadmin/category.html', {'category': categories_list})

@login_required(login_url='adminside:adminlogin')
def addcategory(request):
    return render(request, 'customadmin/addcategory.html')

@login_required(login_url='adminside:adminlogin')
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
        
        return redirect('category:categorymanagement')  
    

    return render(request, 'customadmin/addcategory.html')


@login_required(login_url='adminside:adminlogin')
def edit_savecategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        new_category_name = request.POST.get('category_name')
        if category_id and new_category_name:
            category = get_object_or_404(categories, id=category_id)
            category.category_name = new_category_name
            category.save()
            return redirect('category:categorymanagement')  

    return redirect('category:edit_category', category_id=category_id)


@login_required(login_url='adminside:adminlogin')

def delete_category(request, category_id):
    category = get_object_or_404(categories, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('category:categorymanagement')  
    
    return redirect('category:categorymanagement')  