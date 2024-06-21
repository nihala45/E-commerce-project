from django.shortcuts import render

# Create your views here.
def productdetails(request):
    return render(request,'userside/productsdetails.html')