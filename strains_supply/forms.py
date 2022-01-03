import datetime as dt

from django import forms
from django.db.models import fields
from django.forms import modelformset_factory
from django.forms.widgets import Textarea

from .models import BacteriaType, Source, Supply, CompanyBranch, SupplyContent


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ]


class NumberInput(forms.NumberInput):
    input_type = "number"


class SourceForm(forms.Form):

    source_id = forms.ChoiceField(
        label="Выберите лечебное учреждение",
        required=False,
        widget=forms.Select(attrs={"data-choose-item": "exists"}),
    )
    name = forms.CharField(
        label="Название",
        required=False,
        widget=forms.TextInput(attrs={"data-choose-item": "create"}),
    )
    city = forms.CharField(
        label="Город",
        required=False,
        widget=forms.TextInput(attrs={"data-choose-item": "create"}),
    )

    def clean(self):
        source_id = self.cleaned_data["source_id"]
        name = self.cleaned_data["name"]
        city = self.cleaned_data["city"]
        if source_id == "":
            if not name:
                self.add_error("name", "Заполните название лечебного учреждения")
            if not city:
                self.add_error("city", "Заполните город лечебного учреждения")
        if source_id:
            self.cleaned_data["source_id"] = int(source_id)

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        sources_ = [(s.id, str(s)) for s in Source.objects.all()]
        sources = [("", " + Добавить новое лечебное учреждение")]
        sources.append(("Сохраненные лечебные учреждения", sources_))
        self.fields["source_id"].choices = sources


class DestForm(forms.Form):

    dest_id = forms.ChoiceField(
        label="Филиал назначения",
        required=False,
        widget=forms.Select(attrs={"data-choose-item": "exists"}),
    )
    name = forms.CharField(
        label="Название филиала",
        required=False,
        widget=forms.TextInput(attrs={"data-choose-item": "create"}),
    )

    def clean(self):
        dest_id = self.cleaned_data["dest_id"]
        name = self.cleaned_data["name"]
        if dest_id == 0 and not name:
            self.add_error("name", "Заполните название филиала")
        if dest_id:
            self.cleaned_data["dest_id"] = int(dest_id)

    def __init__(self, *args, **kwargs):
        super(DestForm, self).__init__(*args, **kwargs)
        dests_ = [(c.id, c.name) for c in CompanyBranch.objects.all()]
        dests = [("", " + Добавить филиал")]
        dests.extend(dests_)
        self.fields["dest_id"].choices = dests


class DetailForm(forms.Form):

    suggested_sent_date = forms.DateField(
        label="Предполагаемая дата отправки", widget=DateInput, required=False
    )
    suggested_num = forms.IntegerField(
        label="Предполагаемое количество", widget=NumberInput, required=False
    )


class SuggestingDataForm(DetailForm):
    pass


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ["source", "dest", "suggested_sent_date", "suggested_num"]

        widgets = {"suggested_sent_date": DateInput, "suggested_num": NumberInput}


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ["sent_at", "received_at"]

        widgets = {"sent_at": DateInput, "received_at": DateTimeInput}

    def __init__(self, *args, **kwargs):
        super(ReceiveForm, self).__init__(*args, **kwargs)
        if self.instance.received_at:
            kwargs.update(
                initial={
                    "received_at": self.instance.received_at.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                }
            )
        super(ReceiveForm, self).__init__(*args, **kwargs)
        self.fields["received_at"].required = True


class SupplyContentForm(forms.ModelForm):
    supply = forms.ModelChoiceField(
        queryset=Supply.objects.all(), widget=forms.HiddenInput()
    )

    class Meta:
        model = SupplyContent
        fields = "__all__"


SupplyContentFormSet = modelformset_factory(
    SupplyContent,
    fields=(
        "id",
        "supply",
        "bacteria_type",
        "strain",
    ),
    extra=5,
    can_delete=True,
    can_delete_extra=True,
    widgets={"supply": forms.HiddenInput()},
)


class RemarkForm(forms.ModelForm):
    received_remark = forms.CharField(
        label="Примечание", widget=Textarea, required=False
    )

    class Meta:
        model = Supply
        fields = ["received_remark"]
