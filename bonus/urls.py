from django.urls import path
from .views import *

urlpatterns = [
    path('', BonusList, name='BonusList'),

]
