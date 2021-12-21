from django.shortcuts import redirect, render

from strains_supply import services, utils

from .models import Supply
from .forms import DetailForm, SourceForm, DestForm, SupplyForm


def main_page(request):
    supply_list = Supply.objects.all()
    return render(request, 'strains_supply/main.html',
                  {'supply_list': supply_list})


def supply_new(request):
    step = int(request.GET.get('step', '1'))
    prev = None
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
                dest = services.get_or_create_dest(inserted_by=request.user,
                                                   **form.cleaned_data)
                return redirect(
                    f'/strains_supply/new?step={step + 1}&source={source_id}&dest={dest.id}')
        elif step == 3:
            params = utils.extract_get_param(request)
            source_id = params['source']
            dest_id = params['dest']
            form = DetailForm(request.POST)
            if form.is_valid():
                sent_at = form.cleaned_data['sent_at']
                num = form.cleaned_data['num']
                return redirect(
                    f'/strains_supply/new?step={step + 1}&source={source_id}&dest={dest_id}&num={num}&sent_at={sent_at}')

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
                return redirect('/strains_supply/')
    else:
        if step == 1:
            fields = {}
            source = request.GET.get('source')
            if source:
                fields['source_id'] = int(source)
            form = SourceForm(initial=fields)
        elif step == 2:
            fields = {}
            source = request.GET.get('source')
            dest = request.GET.get('dest')
            if dest:
                fields['dest_id'] = int(dest)
            form = DestForm(initial=fields)
            prev = f'/strains_supply/new?step={step - 1}&source={source}'
        elif step == 3:
            source = request.GET.get('source')
            dest = request.GET.get('dest')
            prev = f'/strains_supply/new?step={step - 1}&source={source}&dest={dest}'
            form = DetailForm()
        else:
            step = 4
            fields = utils.extract_get_param(request)

            source = fields['source']
            dest = fields['dest']
            num = fields['num']
            sent_at = fields['sent_at']
            prev = f'/strains_supply/new?step={step - 1}&source={source}&dest={dest}&num={num}&sent_at={sent_at}'
            form = SupplyForm(initial=fields)

    return render(request, 'strains_supply/edit_supply.html', {
        'form': form,
        'step': step,
        'prev': prev
    })
