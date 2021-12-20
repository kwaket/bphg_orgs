from django.shortcuts import redirect, render

from strains_supply import services

from .models import Supply
from .forms import SourceForm, DestForm, SupplyForm


def main_page(request):
    supply_list = Supply.objects.all()
    return render(request, 'strains_supply/main.html',
                  {'supply_list': supply_list})


def new_supply(request):
    step = int(request.GET.get('step', '1'))
    print(step, '------')
    if request.method == 'POST':
        if step == 1:
            form = SourceForm(request.POST)
            if form.is_valid():
                source = services.get_or_create_source(inserted_by=request.user,
                                                       **form.cleaned_data)
                return redirect(
                    f'/strains_supply/new?step={step + 1}&source={source.id}')
        elif step == 2:
            source_id = request.GET.get('source')
            form = DestForm(request.POST)
            if form.is_valid():
                import ipdb; ipdb.set_trace()
                dest = services.get_or_create_dest(inserted_by=request.user,
                                                   **form.cleaned_data)
                return redirect(
                    f'/strains_supply/new?step={step + 1}&source={source_id}&dest={dest.id}')
        else:
            form = SupplyForm(request.POST)
            if form.is_valid():
                services.create_supply(
                    source=form.cleaned_data['source'],
                    dest=form.cleaned_data['dest'],
                    sent_at=form.cleaned_data['sent_at'],
                    num=form.cleaned_data['num'],
                    inserted_by=request.user
                )
    else:
        if step == 1:
            form = SourceForm()
        elif step == 2:
            form = DestForm()
        else:
            source = request.GET.get('source')
            dest = request.GET.get('dest')

            print(dest, 'dest =====')
            form = SupplyForm(initial={
                'source': services.get_source_by_id(source),
                'dest': services.get_dest_by_id(dest)
            })

    return render(request, 'strains_supply/edit_supply.html', {
        'form': form,
        'step': step
    })
