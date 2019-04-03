from django.shortcuts import render,get_object_or_404
from shop.models import Product
# Create your views here.
def MainPage(request):
    products = Product.objects.filter(available=True)[0:4]
    return render(request, 'main/main.html', {
        'products': products
    })

# Страница с товарами
def Products(request):

    products = Product.objects.filter(available=True)
    return render(request, 'main/products.html', {
        'products': products
    })
# Страница товара
def ProductDetails(request, id):

    product = get_object_or_404(Product, id=id, available=True)

    return render(request, 'main/detail.html',
                  {'product': product})

