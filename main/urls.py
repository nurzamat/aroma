from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage, name='MainPage'),
    path('products',Products,name='Products'),
    path('products/<int:id>', ProductDetails, name='ProductDetails'),

]
