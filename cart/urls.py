from django.urls import path
from .views import *

urlpatterns = [
    path('',CartDetail , name='CartDetail'),
    path('add/<int:product_id>',CartAdd , name='CartAdd'),
    path('remove/<int:product_id>',CartRemove, name='CartRemove')
]
