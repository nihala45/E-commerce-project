from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from category.models import categories
import re
from products.models import newproducts

from logintohome.models import CustomUser

# Create your views here.
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
        
        return redirect('category:category')  

    return render(request, 'customadmin/addcategory.html')

        

