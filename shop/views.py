from django.shortcuts import render,get_object_or_404
from .models import  Product
from cart.forms import CartAddProductForm
# Страница с товарами
def ProductList(request):

    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/list.html', {
        'products': products
    })
# Страница товара
# def ProductDetail(request, id):
#     product = get_object_or_404(Product, id=id,  available=True)
#     return render(request, 'shop/product/deatail.html', {'product': product})

# Страница товара
def ProductDetail(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/deatail.html',
                  {'product': product,
                              'cart_product_form': cart_product_form})