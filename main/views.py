from django.shortcuts import render,get_object_or_404
from shop.models import Product
from .models import News,Testimonials,Sliders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def MainPage(request):
    products = Product.objects.filter(available=True)[0:4]
    main_news=News.objects.order_by('created')[0:3]
    testims=Testimonials.objects.order_by('name')[0:4]
    slides=Sliders.objects.order_by('created')

    return render(request, 'main/main.html', {
        'products': products,'news':main_news,'testims':testims,'slides':slides
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

# Страница с новостями
def NewsList(request):
    news_list=News.objects.order_by('updated')
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render(request, 'main/news.html',{'news':news})

def NewsDetail(request,id):
    item = get_object_or_404(News, id=id)
    return render(request, 'main/newsdetail.html',{'item':item})
def SlideDetail(request,id):
    item = get_object_or_404(Sliders, id=id)
    return render(request, 'main/newsdetail.html',{'item':item})