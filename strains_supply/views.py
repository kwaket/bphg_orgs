from django.shortcuts import render

from .models import Supply
from .forms import SupplyForm


def new_supply(request):
    form = SupplyForm()
    return render(request, 'strains_supply/edit_supply.html', {'form': form})
