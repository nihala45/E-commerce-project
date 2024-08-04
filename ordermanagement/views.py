from django.shortcuts import render, get_object_or_404,redirect
# from cartapp.models import Orders
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from newcart.models import AllOrder
from newcart.models import Ordered_item
from decimal import Decimal


# Create your views here

@login_required(login_url='adminside:adminlogin')
def order_management(request):
    ordered_items = AllOrder.objects.all()
    context = {
        'ordered_items': ordered_items
    }
    return render(request, 'customadmin/ordermanagement.html', context)

@login_required(login_url='adminside:adminlogin')
def admin_ordered_view(request, ord_id):
    all_orders=AllOrder.objects.get(id=ord_id)
    order_items=Ordered_item.objects.filter(order_id=ord_id).order_by('id')
    discount_price=0
    first_addresses = order_items.first().address if order_items.exists() else None
    total_product_quantity = 0
    total_amounts=[]
    
    for item in order_items:
        total_product_quantity += item.product_qty
    discount_price = Decimal(all_orders.discount_amount) / Decimal(total_product_quantity) if total_product_quantity > 0 else Decimal(0)
    for item in order_items:
        
        if item.product.offer:
        
            amount = Decimal(item.product.price) - Decimal(item.product.offer.discount)
            
        else:
            amount = Decimal(item.product.price)
        unit_price = amount - discount_price
        total_amount = unit_price * Decimal(item.product_qty)
        total_amounts.append(total_amount)
    
    context = {
        'all_order': all_orders,
        'order_item':order_items,
        'first_address':first_addresses,
        'total_amounts':total_amounts
    }
    
    
    return render(request, 'customadmin/adminview.html',context)


def status_update(request):
    print('sssdasssssssssssssssssssssssssssssfrwsdtegfcvthedffb45676555555555555555555555s')
    if request.method=='POST':
        item_id=request.POST.get('item_id')
        status=request.POST.get('status')
        ord_id=request.POST.get('ord_id')
        
        ord=Ordered_item.objects.get(id=item_id)
        print('this is item id',item_id)
        ord.status=status
        ord.save()
        print("ffffffffffffffffffffllllllllllllllllllllllllllllllllllllllllllllllllll",ord)
        return redirect(reverse('ordermanagement:admin_ordered_view', args=[ord_id]))
        