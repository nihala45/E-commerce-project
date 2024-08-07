from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from newcart.models import AllOrder
from newcart.models import Ordered_item
from products.models import newproducts
from django.db.models import Sum
from django.db.models import Count
from category.models import categories
# Create your views here.
@never_cache
def adminloginn(request):
    if 'is_superuser' in request.session:
        super_user = request.session['is_superuser']
        return redirect('adminside:dashboard')    
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
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
    order_cash_delevery=AllOrder.objects.filter(payment_method="cash_on_delivery")
    cash_delevery=len(order_cash_delevery)
    order_wallet=AllOrder.objects.filter(payment_method="Wallet")
    wallet_delevery=len(order_wallet)
    order_razor=AllOrder.objects.filter(payment_method="razor_pay")
    razor_delevery=len(order_razor)
    
    
    
    order=Ordered_item.objects.filter(status="Delivered")
    
    products = []
    for i in order:
        products.append(i.product_id)


    product_count = {}


    for product_id in products:
        if product_id in product_count:
            product_count[product_id] += 1
        else:
            product_count[product_id] = 1

    
    sorted_product_count = sorted(product_count.items(), key=lambda item: item[1], reverse=True)
    product1_id = sorted_product_count[0][1]
    prod1_id = sorted_product_count[0][0]
    
    product1=newproducts.objects.get(id=prod1_id)
    
    

    product2_id = sorted_product_count[1][1]
    prod2_id = sorted_product_count[1][0]
    product2=newproducts.objects.get(id=prod2_id)
    
    
    
    product3_id = sorted_product_count[2][1]
    prod3_id = sorted_product_count[2][0]
    
    product3=newproducts.objects.get(id=prod3_id)
    
    
    
    

    delivered_items = Ordered_item.objects.filter(status='Delivered')
     # Annotate each product with its category and count the occurrences
    category_sales = (delivered_items
                  .values('product__category__category_name')  # Group by category name
                  .annotate(sales_count=Count('product'))  # Count products in each category
                  .order_by('-sales_count'))  # Order by sales count descending

# Step 3: Get top 3 categories
    top_3_categories = category_sales[:3]  
    category1 =top_3_categories[0]['product__category__category_name']
    category2 =top_3_categories[1]['product__category__category_name']
    category3 =top_3_categories[2]['product__category__category_name']
    category1_count =top_3_categories[0]['sales_count']
    category2_count =top_3_categories[1]['sales_count']
    category3_count =top_3_categories[2]['sales_count']
    
    
    
    print(top_3_categories,'this is top 3 catttttttttttttttttttttttttttttttttttttttttttttttttttttt',category1,category1_count)     
    # top_selling_categories = (
    #     Ordered_item.objects.filter(status="Delivered")
    #     .values("product__category")
    #     .annotate(total_sold=Sum("product_qty"))
    #     .order_by("-total_sold")[:3]
    # )
    
    # top_selling_products = (
    #     Ordered_item.objects.filter(status="Delivered")
    #     .values("product")
    #     .annotate(total_sold=Sum("product_qty"))
    #     .order_by("-total_sold")[:3]
    # )
    # top_products = []
    # for item in top_selling_products:
    #     product_id = item["product"]
    #     product = newproducts.objects.get(id=product_id)
    #     top_products.append({
    #         'name': product.name,
    #         'total_sold': item['total_sold']
    #     })

    # # Get delivered order IDs
    # delivered_order_ids = Ordered_item.objects.filter(status="Delivered").values_list('order_id', flat=True)
    
    # # Get top payment methods
    # top_payment_methods = (
    #     AllOrder.objects.filter(id__in=delivered_order_ids)
    #     .values('payment_method')
    #     .annotate(count=Count('payment_method'))
    #     .order_by('-count')[:3]
    # )

    # top_selling_categories = (
    #     Ordered_item.objects.filter(status="Delivered")
    #     .values("product__category")
    #     .annotate(total_sold=Sum("product_qty"))
    #     .order_by("-total_sold")[:3]
    # )
    
    # top_categories = []
    # for item in top_selling_categories:
    #     category_id = item["product__category"]
    #     category = categories.objects.get(id=category_id)
    #     top_categories.append({
    #         'category_name': category.category_name,
    #         'total_sold': item['total_sold']
    #     })

    # context = {
    #     "top_products": top_products,
    #     "top_payment_methods": list(top_payment_methods),
    #     "top_categories": top_categories
    # }
    context={
        "cash_delevery":cash_delevery,
        "wallet_delevery":wallet_delevery,
        "razor_delevery":razor_delevery,
        'product1_id':product1_id,
        'product2_id':product2_id,
        'product3_id':product3_id,
        'product1':product1.name,
        'product2':product2.name,
        'product3':product3.name,
        'category1':category1,
        'category2':category2,
        'category3':category3,
        'category1_count':category1_count,
        'category2_count':category2_count,
        'category3_count':category3_count,
        
        
        
        
    }
    
    return render(request, 'customadmin/dashboard.html',context)


@login_required(login_url='adminside:adminlogin')

def logout_view(request):
    if request.session.get('is_superuser'):
        del request.session['is_superuser']  
    logout(request)  
    return redirect('adminside:adminlogin')