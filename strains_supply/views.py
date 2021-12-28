from django.shortcuts import redirect, render

from strains_supply import services, utils

from .forms import (
    DetailForm, ReceiveForm, RemarkForm, SourceForm, DestForm, SupplyContentFormSet,
    SupplyForm
)


def supply_main(request):
    supply_list = services.get_newest_supply_for_user(request.user, limit=10)
    is_moderator = services.is_supply_moderator(request.user)
    return render(request, 'strains_supply/supply_main.html',
                  {'supply_list': supply_list,
                   'is_supply_moderator': is_moderator})


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
                sent_date = form.cleaned_data['suggested_sent_date']
                num = form.cleaned_data['suggested_num']
                return redirect(
                    f'/strains_supply/new?step={step + 1}&source={source_id}&dest={dest_id}&suggested_num={num}&suggested_sent_date={sent_date}')

        else:
            form = SupplyForm(request.POST)
            if form.is_valid():
                services.create_supply(
                    source=form.cleaned_data['source'],
                    dest=form.cleaned_data['dest'],
                    suggested_sent_date=form.cleaned_data['suggested_sent_date'],
                    suggested_num=form.cleaned_data['suggested_num'],
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
            prev = f'/strains_supply/new?step={step - 1}&source={source}'  # TODO: generate url with function
        elif step == 3:
            source = request.GET.get('source')
            dest = request.GET.get('dest')
            prev = f'/strains_supply/new?step={step - 1}&source={source}&dest={dest}'  # TODO: generate url with function
            fields = utils.extract_get_param(request)
            form = DetailForm(initial=fields)
        else:
            step = 4
            fields = utils.extract_get_param(request)

            source = fields['source']
            dest = fields['dest']
            num = fields['suggested_num']
            sent_date = fields['suggested_sent_date']
            prev = f'/strains_supply/new?step={step - 1}&source={source}&dest={dest}&suggested_num={num}&suggested_sent_date={sent_date}'  # TODO: generate url with function
            form = SupplyForm(initial=fields)

    return render(request, 'strains_supply/supply_edit.html', {
        'form': form,
        'step': step,
        'prev': prev
    })


def receive_supply(request, pk, step):
    supply = services.get_supply(pk=pk)
    if step == 1:
        if request.method == "POST":
            form = ReceiveForm(request.POST)
            if form.is_valid():
                supply = services.receive_supply(supply=supply, user=request.user,
                    **form.cleaned_data)
                return redirect('receive_supply', pk=supply.pk, step=step + 1)
        else:
            form = ReceiveForm()
        return render(request, 'strains_supply/receive_supply.html', {
            'supply': supply,
            'form': form,
            'step': step
        })
    elif step == 2:
        supply = services.get_supply(pk=pk)
        if request.method == "POST":
            formset = SupplyContentFormSet(request.POST)
            if formset.is_valid():
                supply = services.unpack_supply(formset.cleaned_data)
                return redirect('receive_supply', pk=supply.pk, step=step + 1)
        else:
            formset = SupplyContentFormSet(
                initial=[{'supply': supply} for _ in range(3)])
        return render(request, 'strains_supply/receive_supply.html', {
            'supply': supply,
            'form': formset,
            'step': step,
        })
    elif step == 3:
        supply = services.get_supply(pk=pk)
        if request.method == "POST":
            form = RemarkForm(request.POST)
            if form.is_valid():
                supply = services.add_remark_to_supply(supply, form.cleaned_data)
                return redirect('supply_main')
        else:
            form = RemarkForm()
        return render(request, 'strains_supply/receive_supply.html', {
            'supply': supply,
            'form': form,
            'step': step
        })
