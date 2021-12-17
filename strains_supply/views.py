from django.shortcuts import render

from .models import Supply
from .forms import SupplyForm


def main_page(request):
    supply_list = Supply.objects.all()
    return render(request, 'strains_supply/main.html',
                  {'supply_list': supply_list})

def new_supply(request):
    form = SupplyForm()
    return render(request, 'strains_supply/edit_supply.html', {'form': form})
