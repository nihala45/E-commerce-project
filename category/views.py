from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from category.models import categories
import re
from products.models import newproducts

from logintohome.models import CustomUser 

# Create your views here.
def categorymanagement(request):
    categoryy = categories.objects.all()
    print(categoryy,"ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    return render(request, 'customadmin/category.html', {'cat': categoryy})

def addcategory(request):
    return render(request, 'customadmin/addcategory.html')

def savecategory(request):
    
    if request.method == 'POST':
        name = request.POST['category']
        print('CATEGORYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        
        
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

        
def edit_category(request, category_id):
    category = categories.objects.get(id=category_id)
    context = {
        'category_name': category.category_name,
        'category_id': category.id, 
    }
    return render(request, 'customadmin/editcategory.html', context)

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

def delete_category(request, category_id):
    category = get_object_or_404(categories, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('category:categorymanagement')  
    
    return redirect('category:categorymanagement')  