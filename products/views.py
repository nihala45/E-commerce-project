from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from category.models import categories
# from .models import varients
import base64
import re
from products.models import newproducts
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from offermanagement.models import Offer



# Create your views here.
@login_required(login_url='adminside:adminlogin')
def products(request):
    productss=newproducts.objects.all().order_by('-id')
    return render(request,'customadmin/products.html',{'products':productss})

@login_required(login_url='adminside:adminlogin')

def addproduct(request):
    categoryy=categories.objects.all()
    offers=Offer.objects.all()
    return render(request,'customadmin/addproduct.html',{'cat':categoryy,'off':offers})


@login_required(login_url='adminside:adminlogin')

def saveproducts(request):
    if request.method=='POST':
        name=request.POST['product_name']
        category_id = request.POST['category']
        description=request.POST['description']
        price=request.POST['price']
        
        
        category = categories.objects.get(id=category_id)
        
       
        img1 = request.FILES["img1"] if "img1" in request.FILES else None
        img2 = request.FILES["img2"] if "img2" in request.FILES else None
        img3 = request.FILES["img3"] if "img3" in request.FILES else None
        img4 = request.FILES["img4"] if "img4" in request.FILES else None 
        small=request.POST['small_quantity']
        medium=request.POST['medium_quantity']
        large=request.POST['large_quantity']
        offer_id = request.POST.get('offer', None)
        
        offer = Offer.objects.get(id=offer_id) if offer_id else None
        
        products2=newproducts(
           name=name,
           category=category,
           description=description,
           price=price,
           image1=img1,
           image2=img2,
           image3=img3,
           image4=img4,
           small=small,
           medium=medium,
           large=large,
           offer=offer,
        )    
        products2.save()
        return redirect('products:products')


@login_required(login_url='adminside:adminlogin')
      
def product_delete(request, prod_id):
    pro = get_object_or_404(newproducts, id=prod_id)
    if request.method == 'POST':
        pro.delete()
        return redirect('products:products')
    return redirect('products:products')



@login_required(login_url='adminside:adminlogin')

def product_editpage(request, prod_id):
    product = newproducts.objects.get(id=prod_id)
    catyy = categories.objects.all()
    offer_details=Offer.objects.all()
    return render(request, 'customadmin/editproduct.html', {'product': product, 'catyy': catyy,'offers':offer_details})


@login_required(login_url='adminside:adminlogin')

def product_editsave(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')

        editname = request.POST.get('productname')
        editdescription = request.POST.get('descri')
        editcategory = request.POST.get('cat')
        editprice = request.POST.get('pri')
        editimage1 = request.FILES.get('new_image1') if 'new_image1' in request.FILES else None
        editimage2 = request.FILES.get('new_image2') if 'new_image2' in request.FILES else None
        editimage3 = request.FILES.get('new_image3') if 'new_image3' in request.FILES else None
        editimage4 = request.FILES.get('new_image4') if 'new_image4' in request.FILES else None
        editsmall = request.POST.get('smallquantity')
        editmedium = request.POST.get('mediumquantity')
        editlarge = request.POST.get('largequantity')
        editoffer = request.POST.get('off')
        
        
        
        pro = newproducts.objects.get(id=prod_id)
        pro.name = editname
        pro.description = editdescription
        
        category = categories.objects.get(id=editcategory)
        pro.category = category
        
       
        offer = Offer.objects.get(id=editoffer) if editoffer else None
        pro.offer = offer
        
        pro.price = editprice
        if editimage1:
            pro.image1 = editimage1
        if editimage2:
            pro.image2 = editimage2
        if editimage3:
            pro.image3 = editimage3
        if editimage4:
            pro.image4 = editimage4
        pro.small = editsmall
        pro.medium = editmedium
        pro.large = editlarge
        
        pro.save()
        
        return redirect('products:products')
    else:
        return redirect('products:products')
            
            

    
        
        
        