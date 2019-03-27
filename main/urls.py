from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage, name='MainPage'),
    path('<int:id>', ProductDetails, name='ProductDetails'),

]
