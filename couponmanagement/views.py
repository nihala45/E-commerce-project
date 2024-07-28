from django.shortcuts import render,redirect
from couponmanagement.models import Coupon
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


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
        amount = request.POST.get('amount')
        
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
            critiria_amount=amount,
            date=date,
            expiry_date=expireDate
        )
        offer.save()

        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def get_coupon(request,coupon_id):
    try:
        coupon=Coupon.objects.get(id=coupon_id)
        date = {
            'name': coupon.name,
            'code': coupon.code,
            'percentage':coupon.percentage,
            'critiria_amount':coupon.critiria_amount,
            'cash_date':coupon.date,
            'expire_date':coupon.expiry_date,
        }
        return JsonResponse(date)
    except Coupon.DoesNotExist:
        return JsonResponse({'status':'error', 'message':'Offer not found'},status=400)
    
def editCoupon(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        name = request.POST.get('couponName')
        code = request.POST.get('code')
        percentage = request.POST.get('percentage')
        amount = request.POST.get('amount')
        
        cashDate = request.POST.get('cashDate')
        expireDate = request.POST.get('expireDate')

        if not all([coupon_id, name, code, percentage, cashDate, expireDate]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        coupon = get_object_or_404(Coupon, id=coupon_id)
        coupon.name = name
        coupon.code = code
        coupon.percentage = percentage
        coupon.critiria_amount = amount
        
        coupon.date = cashDate
        coupon.expiry_date = expireDate

        coupon.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
 


def remove_coupon(request,coupon_id):
    coupon=Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('couponmanagement:coupons')