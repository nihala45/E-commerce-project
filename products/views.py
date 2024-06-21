from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import categories
# from .models import varients
import base64
import re
from .models import newproducts




# Create your views here.

def products(request):
    productss=newproducts.objects.all()
    
    return render(request,'customadmin/products.html',{'products':productss})

def addproduct(request):
    categoryy=categories.objects.all()
    return render(request,'customadmin/addproduct.html',{'categories':categoryy})

def saveproducts(request):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )
    if request.method=='POST':
        name=request.POST['productname']
        category_id = request.POST['productcategory']
        description=request.POST['productdescription']
        price=request.POST['productprice']
        if not re.match("^[A-Za-z]+$", name):
            messages.error(request, "Product name should only contain letters without spaces or numbers.")
            return redirect('addproduct') 
        category = categories.objects.get(id=category_id)

        if "croppedImageData" in request.POST:
            img1 = request.POST["croppedImageData"]

            
            if img1:
                format, imgstr = img1.split(";base64,")
                ext = re.search(r"/(.*?)$", format).group(1)

               
                decoded_file = base64.b64decode(imgstr)
                img_file = ContentFile(decoded_file, name=f"cropped_image.{ext}")
        img7 = request.FILES["img1"] if "img1" in request.FILES else None
                
        img2 = request.FILES["img2"] if "img2" in request.FILES else None
        img3 = request.FILES["img3"] if "img3" in request.FILES else None
        img4 = request.FILES["img4"] if "img4" in request.FILES else None 
        print(category,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        products2=newproducts(
           name=name,
           category=category,
           description=description,
           price=price,
           image1=img7,
           image2=img2,
           image3=img3,
           image4=img4,
           
        )    
        products2.save()
        return redirect('products:products')

      
def addvarient(request):
    print('ADD VARIENT FUNCTION IS WORKING')
    # if request.method == 'POST':
    #     q1 = request.POST['smallQuantity']
    #     q2 = request.POST['mediumQuantity']
    #     q3 = request.POST['largeQuantity']
    #     print(q1,q2,q3)
    #     already=newproducts.objects.get(product_id=prod_id)
    #     if already:
    #         already.small=q1
    #         already.medium=q2
    #         already.large=q2
    #         already.save()
    # print(prod_id)
        
        
        
    return redirect('products:products')

# def varientreport(request):
#     report=varients.objects.all()
#     return render(request,'customadmin/products.html',{'report':report})



# def varientreport(request):
#     report=varients.objects.all()
#     return render(request,'customadmin/products.html',{'report':report})    