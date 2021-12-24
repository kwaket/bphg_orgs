import datetime as dt

from django import forms
from django.forms.widgets import TextInput, Textarea

from .models import Source, Strain, Supply, CompanyBranch


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    format = "%d.%m.%Y %H:%M:%S %Z"


class NumberInput(forms.NumberInput):
    input_type = 'number'


class SourceForm(forms.Form):

    source_id = forms.ChoiceField(label='Выберите лечебное учреждение',
                                  required=False, widget=forms.Select(
                                      attrs={"data-choose-item": "exists"}
                                  ))
    name = forms.CharField(label='Название', required=False,
        widget=forms.TextInput(attrs={"data-choose-item": "create"}))
    city = forms.CharField(label='Город', required=False,
        widget=forms.TextInput(attrs={"data-choose-item": "create"}))

    def clean(self):
        source_id = self.cleaned_data['source_id']
        name = self.cleaned_data['name']
        city = self.cleaned_data['city']
        if source_id == '':
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
        sources.append(
            ('Сохраненные лечебные учреждения', sources_))
        self.fields['source_id'].choices = sources


class DestForm(forms.Form):

    dest_id = forms.ChoiceField(label='Филиал назначения', required=False,
                                widget=forms.Select(
                                      attrs={"data-choose-item": "exists"}
                                  ))
    name = forms.CharField(label='Название филиала', required=False,
                           widget=forms.TextInput(
                                      attrs={"data-choose-item": "create"}
                                  ))

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


class DetailForm(forms.Form):

    suggested_sent_date = forms.DateField(label='Предполагаемая дата отправки',
                             widget=DateInput, required=False)
    suggested_num = forms.IntegerField(label='Предполагаемое количество',
                             widget=NumberInput, required=False)


class SupplyForm(forms.ModelForm):

    class Meta:
        model = Supply
        fields = ['source', 'dest', 'suggested_sent_date', 'suggested_num']

        widgets = {
            'suggested_sent_date': DateInput,
            'suggested_num': NumberInput
        }


class ReceiveForm(forms.Form):
    sent_at = forms.DateField(label='Фактическая дата отправки',
                              required=False,
                              help_text="Необязательное поле",
                              widget=DateInput)
    received_at = forms.DateTimeField(label='Дата получения',
                                      widget=DateTimeInput,
                                      initial=dt.datetime.now)


class UnpackForm(forms.Form):

    def clean(self):
        for key, val in self.cleaned_data.items():
            if not val:
                continue
            self.cleaned_data[key] = int(val)
        return self.cleaned_data

    @property
    def dynamic_fields(self):
        fields = {}
        for k, v in self.data.items():
            if k == 'csrfmiddlewaretoken':
                continue
            fields[k] = v
        return fields

    def _clean_fields(self):
        self.cleaned_data = self.dynamic_fields

    def __init__(self, *args, **kwargs):
        super(UnpackForm, self).__init__(*args, **kwargs)
        strains = Strain.objects.all()
        for s in strains:
            self.fields[s.pk] = forms.CharField(
                label=s.name,
                initial=0,
                widget=NumberInput)


class RemarkForm(forms.Form):

    remark = forms.CharField(label='Комментарий', widget=Textarea,
                             required=False)
