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
    productss=newproducts.objects.all()
    
    # print(productss)
   
    
    
    return render(request,'customadmin/products.html',{'products':productss})

@login_required(login_url='adminside:adminlogin')

def addproduct(request):
    categoryy=categories.objects.all()
    offers=Offer.objects.all()
    return render(request,'customadmin/addproduct.html',{'cat':categoryy,'off':offers})


@login_required(login_url='adminside:adminlogin')

def saveproducts(request):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )
    if request.method=='POST':
        print('inside of the post method')
        name=request.POST['product_name']
        category_id = request.POST['category']
        description=request.POST['description']
        price=request.POST['price']
        
        # if not re.match("^[A-Za-z]+$", name):
            
        #     messages.error(request, "Product name should only contain letters without spaces or numbers.")
        #     return redirect('products:saveproducts') 
        category = categories.objects.get(id=category_id)
        
        
        # if "croppedImageData" in request.POST:
        #     img1 = request.POST["croppedImageData"]
        #     if img1:
        #         format, imgstr = img1.split(";base64,")
        #         ext = re.search(r"/(.*?)$", format).group(1)    
        #         decoded_file = base64.b64decode(imgstr)
        #         img_file = ContentFile(decoded_file, name=f"cropped_image.{ext}")
        img1 = request.FILES["img1"] if "img1" in request.FILES else None
        img2 = request.FILES["img2"] if "img2" in request.FILES else None
        img3 = request.FILES["img3"] if "img3" in request.FILES else None
        img4 = request.FILES["img4"] if "img4" in request.FILES else None 
        small=request.POST['small_quantity']
        medium=request.POST['medium_quantity']
        large=request.POST['large_quantity']
        offer_id=request.POST['offer']
        offer=Offer.objects.get(id=offer_id)
        
        
        
        print(category,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
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
    print(vars(product),"gjyhgbvc ",product.id,"iddddddddddddddddddd")
    return render(request, 'customadmin/editproduct.html', {'product': product, 'catyy': catyy,'offers':offer_details})


@login_required(login_url='adminside:adminlogin')

def product_editsave(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        print(prod_id,'niahfiahfiahfiahfiahiahfhu')
        

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
        
        
        print(editcategory,'EDIT CATEGORUYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        pro = newproducts.objects.get(id=prod_id)
        pro.name = editname
        pro.description = editdescription
        # pro.category = editcategory
        category = categories.objects.get(id=editcategory)
        offers = Offer.objects.get(id=editoffer)
        
        pro.category = category
        

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
        pro.offer = offers
        

        pro.save()
        

        return redirect('products:products')
    else:
        return redirect('products:products')
    
        
            
            
        
# @login_required(login_url='adminside:adminlogin')

# def search_for_product(request):
#     if request.method == 'POST':
#         query = request.POST.get('query')
        
#         products = newproducts.objects.filter(name__icontains=query)
    
#         return render(request, 'products.html', products)
    
        
        
        