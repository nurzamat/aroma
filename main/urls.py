from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage, name='MainPage'),

]
