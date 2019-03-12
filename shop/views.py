from django.shortcuts import render,get_object_or_404
from .models import  Product
from cart.forms import CartAddProductForm


# Страница с товарами
def ProductList(request):
    user = request.user
    node = user.node
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/list.html', {
        'products': products, 'node': node
    })
# Страница товара
# def ProductDetail(request, id):
#     product = get_object_or_404(Product, id=id,  available=True)
#     return render(request, 'shop/product/deatail.html', {'product': product})


# Страница товара
def ProductDetail(request, id):
    user = request.user
    node = user.node
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/deatail.html',
                  {'product': product, 'cart_product_form': cart_product_form, 'node': node})

