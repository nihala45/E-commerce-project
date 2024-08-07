from django.shortcuts import render,redirect
from django.http import JsonResponse
from offermanagement.models import Offer
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required




@login_required(login_url='adminside:adminlogin')
def offermanagement(request):
    offer_details_all = Offer.objects.all()
    return render(request, 'customadmin/offermanagement.html', {'offer_details_all': offer_details_all})


@login_required(login_url='adminside:adminlogin')
def Addoffer(request):
    if request.method == 'POST':
        offer_name = request.POST.get('offerName')
        discount = request.POST.get('discount')
        cash_date = request.POST.get('cashDate')
        expire_date = request.POST.get('expireDate')
        if Offer.objects.filter(name=offer_name).exists():
            return JsonResponse({'status': 'error', 'message': 'name already exists.'}, status=400)

        
        offer = Offer(
            name=offer_name,
            discount=discount,
            active_date=cash_date,
            expiry_date=expire_date
        )
        offer.save()


        return JsonResponse({'status': 'success'})
    
@login_required(login_url='adminside:adminlogin')     
def get_offer(request, offer_id):
    try:
        offer = Offer.objects.get(id=offer_id)
        data = {
            'name': offer.name,
            'discount': offer.discount,
            'cash_date': offer.active_date,
            'expire_date': offer.expiry_date,
        }
        return JsonResponse(data)
    except Offer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Offer not found'}, status=404)
    

@login_required(login_url='adminside:adminlogin')
def editSubmitOffer(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        name = request.POST.get('offerName')
        discount = request.POST.get('discount')
        cash_date = request.POST.get('cashDate')
        expire_date = request.POST.get('expireDate')

        offer = get_object_or_404(Offer, id=offer_id)

    
        offer.name = name
        offer.discount = discount
        offer.active_date = cash_date
        offer.expiry_date = expire_date

        
        offer.save()

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required(login_url='adminside:adminlogin')
def remove_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    offer.delete()
    return redirect('offermanagement:offermanagement')

        
    