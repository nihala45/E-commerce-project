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




# Create your views here.

def products(request):
    productss=newproducts.objects.all()
    # print(productss)
   
    
    
    return render(request,'customadmin/products.html',{'products':productss})

def addproduct(request):
    categoryy=categories.objects.all()
    return render(request,'customadmin/addproduct.html',{'cat':categoryy})

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
        )    
        products2.save()
        return redirect('products:products')


      
def product_delete(request, prod_id):
    pro = get_object_or_404(newproducts, id=prod_id)
    if request.method == 'POST':
        pro.delete()
        return redirect('products:products')
    return redirect('products:products')


def product_editpage(request, prod_id):
    product = newproducts.objects.get(id=prod_id)
    catyy = categories.objects.all()
    print(vars(product),"gjyhgbvc ",product.id,"iddddddddddddddddddd")
    return render(request, 'customadmin/editproduct.html', {'product': product, 'catyy': catyy})


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
        
        print(editcategory,'EDIT CATEGORUYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        pro = newproducts.objects.get(id=prod_id)
        pro.name = editname
        pro.description = editdescription
        # pro.category = editcategory
        category = categories.objects.get(id=editcategory)
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

        pro.save()
        

        return redirect('products:products')
    else:
        return redirect('products:products')
    
        
            
            
        
        
        
        
        