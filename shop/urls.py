from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList, name='ProductList'),
    path('<int:id>',ProductDetail, name='ProductDetail'),

]
