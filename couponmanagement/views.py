from django.shortcuts import render,redirect
from couponmanagement.models import Coupon
from django.http import JsonResponse

# Create your views here.
def coupon(request):
    coupons = Coupon.objects.all()
    return render(request, 'customadmin/couponmanagement.html', {'coupons': coupons})
from django.http import JsonResponse
from .models import Coupon

def Addcoupon(request):
    if request.method == 'POST':
        # Extract POST data
        couponName = request.POST.get('couponName')
        code = request.POST.get('code')
        percentage = request.POST.get('percentage')
        date = request.POST.get('date')
        expireDate = request.POST.get('expireDate')

        
        if Coupon.objects.filter(code=code).exists():
            return JsonResponse({'status': 'error', 'message': 'Coupon code already exists.'}, status=400)
        if Coupon.objects.filter(name=couponName).exists():
            return JsonResponse({'status': 'error', 'message': 'Coupon with this name already exists.'}, status=400)

       
        offer = Coupon(
            name=couponName,
            code=code,
            percentage=percentage,
            date=date,
            expiry_date=expireDate
        )
        offer.save()

        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def remove_coupon(request,coupon_id):
    coupon=Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('couponmanagement:coupon')