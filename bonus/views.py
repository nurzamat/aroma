from django.shortcuts import render
from account.models import Bonus

# Create your views here.
def BonusList(request):
    bonus=Bonus.objects.all()
    return  render(request,'bonus/bonusview.html',{'bonuses':bonus})
