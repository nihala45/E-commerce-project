from django.shortcuts import render, get_object_or_404,redirect
from cartapp.models import Orders
from django.urls import reverse
# Create your views here
def order_management(request):
    ordered_items = Orders.objects.all()
    context = {
        'ordered_items': ordered_items
    }
    return render(request, 'customadmin/ordermanagement.html', context)

def admin_ordered_view(request, ord_id):
    item = get_object_or_404(Orders, id=ord_id)
    cont = {
        'item': item
    }
    return render(request, 'customadmin/adminview.html', cont)

def status_update(request):
    if request.method=='POST':
        item_id=request.POST.get('item_id')
        status=request.POST.get('status')
        ord=Orders.objects.get(id=item_id)
        ord.status=status
        ord.save()
        
        return redirect(reverse('ordermanagement:admin_ordered_view', args=[item_id]))
        