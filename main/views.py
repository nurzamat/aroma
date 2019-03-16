from django.shortcuts import render
from shop.models import Product
# Create your views here.
def MainPage(request):
    products = Product.objects.filter(available=True)
    return render(request, 'main/main.html', {
        'products': products
    })

