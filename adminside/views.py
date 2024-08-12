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
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
from django.db.models.functions import TruncYear
from django.utils.timezone import now
from datetime import datetime
from datetime import datetime, timedelta
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
    order_cash_delevery=AllOrder.objects.filter(payment_method="cash_on_delivery")
    cash_delevery=len(order_cash_delevery)
    order_wallet=AllOrder.objects.filter(payment_method="Wallet")
    wallet_delevery=len(order_wallet)
    order_razor=AllOrder.objects.filter(payment_method="razor_pay")
    razor_delevery=len(order_razor)
    
    
    
    current_date = now()
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    
    
    
    
    current_date = datetime.now()
    current_year = current_date.year
    current_month_number = current_date.month
    current_month_name = current_date.strftime('%B')
    current_time = current_date.strftime('%H:%M:%S')
    
    total_delivered_sales_yearly = AllOrder.objects.filter(
        id__in=Ordered_item.objects.filter(status='Delivered').values('order_id'),
        order_date__year=current_year
    ).aggregate(total_sales=Sum('total_amount'))

    
    delivered_sales_total_yearly = total_delivered_sales_yearly.get('total_sales', 0) or 0

    
    current_month_sales = AllOrder.objects.filter(
        id__in=Ordered_item.objects.filter(status='Delivered').values('order_id'),
        order_date__year=current_year,
        order_date__month=current_month_number
    ).aggregate(total_sales=Sum('total_amount'))

    
    delivered_sales_total_monthly = current_month_sales.get('total_sales', 0) or 0

    

    
    
    today_sales = AllOrder.objects.filter(
        id__in=Ordered_item.objects.filter(status='Delivered').values('order_id'),
        order_date=current_date.date()
    ).aggregate(total_sales=Sum('total_amount'))

    
    delivered_sales_today = today_sales.get('total_sales', 0) or 0
    
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
    
    category_sales = (delivered_items
                  .values('product__category__category_name')  
                  .annotate(sales_count=Count('product'))  
                  .order_by('-sales_count'))  


    top_3_categories = category_sales[:3]  
    category1 =top_3_categories[0]['product__category__category_name']
    category2 =top_3_categories[1]['product__category__category_name']
    category3 =top_3_categories[2]['product__category__category_name']
    category1_count =top_3_categories[0]['sales_count']
    category2_count =top_3_categories[1]['sales_count']
    category3_count =top_3_categories[2]['sales_count']
    
    delivered_orders = AllOrder.objects.filter(
        id__in=Ordered_item.objects.filter(status='Delivered').values('order_id')
    )
    chart_value=[]
    chart_lable=[]
    if request.method == 'GET':
        time_range=request.GET.get('time_range')
        if time_range == 'monthly':
            monthly_sales = (delivered_orders
            .annotate(month=TruncMonth('order_date'))
            .values('month')
            .annotate(total_sales=Sum('total_amount'))
            .order_by('month')
            )

    
            sales_per_month = {calendar.month_name[i]: 0 for i in range(1, 13)}

            print(monthly_sales,"monthly salesasfdnsvljknsdjklvnajlsdnvljk")
            month_item=[]
            for entry in monthly_sales:
                month_name = entry['month'].strftime('%B')
                sales_per_month[month_name] = entry['total_sales']
        
        
                january_sales = sales_per_month['January']
                february_sales = sales_per_month['February']
                march_sales = sales_per_month['March']
                april_sales = sales_per_month['April']
                may_sales = sales_per_month['May']
                june_sales = sales_per_month['June']
                july_sales = sales_per_month['July']
                august_sales = sales_per_month['August']
                september_sales = sales_per_month['September']
                october_sales = sales_per_month['October']
                november_sales = sales_per_month['November']
                december_sales = sales_per_month['December']
        
            chart_value=[january_sales,february_sales,march_sales,april_sales,may_sales,june_sales,july_sales,august_sales,september_sales,october_sales,november_sales,december_sales]
            chart_lable=['January','February','March','April','May','June','July','August','September','October','Novermber','December']
        else:
        
            yearly_sales = (delivered_orders
                .annotate(year=TruncYear('order_date'))
                .values('year')
                .annotate(total_sales=Sum('total_amount'))
                .order_by('year')
            )

    
            sales_per_year = {year: 0 for year in range(2022, 2025)}

            print(yearly_sales, "Yearly Sales")

    
            for entry in yearly_sales:
                year = entry['year'].year
                sales_per_year[year] = entry['total_sales']

    
            sales_2022 = sales_per_year[2022]
            sales_2023 = sales_per_year[2023]
            sales_2024 = sales_per_year[2024]  

    
            chart_value = [sales_2022, sales_2023, sales_2024]
            chart_lable = ['2022', '2023', '2024']

    
        
    
    
        
    print(chart_lable)
    print(".......................................................................")
    print(chart_value)
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
        'chartValue':chart_value,
        'chartLabel':chart_lable,
        'current_month_name': current_month_name,
        'current_month_sales': current_month_sales,
        'today_sales': today_sales,
        'current_time': current_time,
        'delivered_sales_total_yearly': delivered_sales_total_yearly,
        'current_year':current_year,
        'current_date':current_date,
        'delivered_sales_total_monthly':delivered_sales_total_monthly,
        'delivered_sales_today':delivered_sales_today,
        
        
    }
    
    return render(request, 'customadmin/dashboard.html',context)


@login_required(login_url='adminside:adminlogin')

def logout_view(request):
    if request.session.get('is_superuser'):
        del request.session['is_superuser']  
    logout(request)  
    return redirect('adminside:adminlogin')