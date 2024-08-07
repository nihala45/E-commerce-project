from django.shortcuts import render
from newcart.models import AllOrder
from newcart.models import Ordered_item
from decimal import Decimal
from products.models import newproducts
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, date

def salesReport(request):
    delivered_items = Ordered_item.objects.filter(status="Delivered")
    if request.method == 'GET':
        time_range = request.GET.get('time_range')
        if time_range:
            now = timezone.now()
            if time_range:
                if time_range == 'yearly':
                    start_date = now.replace(month=1,day=1)
                    end_date = (start_date.replace(year=now.year+1) - timedelta(days=1))
                elif time_range == 'monthly':
                    start_date = now.replace(day=1)
                    end_date =(start_date.replace(month=now.month + 1) - timedelta(days=1))
                elif time_range == 'weekly':
                    start_date = now - timedelta(days=now.weekday()) 
                    end_date = now 
                else:
                    start_date = None
                    end_date = None
                    
                if start_date and end_date:
                    print(len(delivered_items),"staartinggggggggg")
                    delivered_items = delivered_items.filter(order__order_date__range=(start_date,end_date))
            
            
    if request.method == 'POST':
        start_date_str = request.POST.get('start-date')
        end_date_str = request.POST.get('end-date')

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                # Handle the error if the date format is incorrect
                print("Date format is incorrect")
                start_date = None
                end_date = None

            if start_date and end_date:
                delivered_items = delivered_items.filter(order__order_date__range=(start_date, end_date))
                print(len(delivered_items), "items found in the specified date range.")
    payment_methods = []
    date_lst = []
    product_ids = []
    order_ids=[]
    user_ids=[]
    discount=[]
    amounts=[]
    item_status=[]
    print(len(delivered_items),"topppppppppppppppppppppppppppppppppppppp")
    for item in delivered_items:
        order = AllOrder.objects.filter(id=item.order_id).first()
        if order:
            item_status.append(item.status)
            discount_amount=order.discount_amount
            user_ids.append(item.address.address_name)
            order_ids.append(order.id)
            # product_ids.append(item.product_id)
        
            payment_methods.append(order.payment_method)
            date_lst.append(order.order_date)
            if item.product.offer:
                amount=item.product.price-item.product.offer.discount
            else:
                amount=item.product.price
            
            
            ord=Ordered_item.objects.filter(order_id=order.id)
            dis_quantity=0
            for i in ord:
                dis_quantity+=i.product_qty
            dis=(discount_amount) /(dis_quantity)
            discount.append(dis)
            
            total_amount=(Decimal(amount) - Decimal(dis) )* Decimal(item.product_qty)
            total_amount = total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            amounts.append(total_amount)
            discount_amount=0
    
    totalamount=0
    totalsales=len(amounts)
    for i in amounts:
        totalamount+=i
    combined_data = zip(order_ids, user_ids,date_lst,amounts,item_status,payment_methods)
    
    
    
    
    print(len(delivered_items),'nihaaaaalaaaaaaaaaaa')
    
        
    context = {
        'combined_data': combined_data,
        'totalsales':totalsales,
        'totalamount':totalamount,
    }
    
    return render(request, 'customadmin/sales.html', context)


        
        