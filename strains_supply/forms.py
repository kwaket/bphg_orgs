from django import forms
from django.db import models
from django.forms import widgets

from .models import Source, Supply, CompanyBranch


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.NumberInput):
    input_type = 'number'


class SourceForm(forms.Form):

    source_id = forms.ChoiceField(label='Выберите лечебное учреждение')
    name = forms.CharField(label='Название', required=False)
    city = forms.CharField(label='Город', required=False)

    def clean(self):
        source_id = self.cleaned_data['source_id']
        name = self.cleaned_data['name']
        city = self.cleaned_data['city']
        if source_id == 0:
            if not name:
                self.add_error('name', 'Заполните название лечебного учреждения')
            if not city:
                self.add_error('city', 'Заполните город лечебного учреждения')
        if source_id:
            self.cleaned_data['source_id'] = int(source_id)

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        sources_ = [(s.id, str(s)) for s in Source.objects.all()]
        sources = [('', ' + Добавить новое лечебное учреждение')]
        sources.extend(sources_)
        self.fields['source_id'].choices = sources


class DestForm(forms.Form):

    dest_id = forms.ChoiceField(label='Филиал назначения')
    name = forms.ChoiceField(label='Название филиала', required=False)

    def clean(self):
        dest_id = self.cleaned_data['dest_id']
        name = self.cleaned_data['name']
        if dest_id == 0 and not name:
            self.add_error('name', 'Заполните название филиала')
        if dest_id:
            self.cleaned_data['dest_id'] = int(dest_id)

    def __init__(self, *args, **kwargs):
        super(DestForm, self).__init__(*args, **kwargs)
        dests_ = [(c.id, c.name) for c in CompanyBranch.objects.all()]
        dests = [('', ' + Добавить филиал')]
        dests.extend(dests_)
        self.fields['dest_id'].choices = dests


class SupplyForm(forms.ModelForm):

    class Meta:
        model = Supply
        fields = ['source', 'dest', 'sent_at', 'num']

        widgets = {
            'sent_at': DateInput,
            'num': NumberInput
        }
