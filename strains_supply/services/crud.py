from typing import Union, List

from django import forms
from django.contrib.auth.models import User
from django.db.models import Model

import datetime as dt

from strains_supply.models import CompanyBranch, Source, City, Supply, SupplyContent

from .. import utils


def _fill_meta_fields(
    model: Model,
    inserted_by: User,
    updated_by: User = None,
    updated_at: dt.datetime = None,
):
    model.inserted_by = inserted_by
    model.updated_by = updated_by or inserted_by
    if updated_at:
        model.updated_at = updated_at
    return model


def get_city(city_id: int) -> City:
    return City.objects.get(pk=city_id)


def create_city(name: str, inserted_by: User) -> City:
    alias = utils.get_alias(name)
    city = City.objects.filter(alias=alias).first()
    if city:
        return city
    city = City(name=name, alias=alias)
    city = _fill_meta_fields(city, inserted_by)
    city.save()
    return city


def get_or_create_city(
    city_id: int = None, name: str = None, inserted_by: User = None
) -> City:
    if city_id:
        return get_city(city_id)
    return create_city(name, inserted_by)


def get_source(source_id: int) -> Source:
    print("source_id", source_id)
    return Source.objects.get(pk=source_id)


def create_source(name: str, city: City, inserted_by: User) -> Source:
    source = Source.objects.create(name=name, city=city)
    source = _fill_meta_fields(source, inserted_by)
    source.save()
    return source


def get_or_create_source(
    source_id: int = None, name: str = None, city: City = None, inserted_by: User = None
) -> Source:
    if source_id:
        return get_source(source_id)
    return create_source(name, city, inserted_by)


def get_dest(dest_id: int) -> CompanyBranch:
    return CompanyBranch.objects.get(pk=dest_id)


def create_dest(name: str, inserted_by: User) -> CompanyBranch:
    dest = CompanyBranch(name=name)
    dest = _fill_meta_fields(dest, inserted_by)
    dest.save()
    return dest


def get_or_create_dest(
    dest_id: int = None, name: str = None, inserted_by: User = None
) -> CompanyBranch:
    if dest_id:
        return get_dest(dest_id)
    alias = utils.get_alias(name)
    dest = CompanyBranch.objects.filter(alias=alias).first()
    if dest:
        return dest
    return create_dest(name, inserted_by)


def get_supply(supply_id: int) -> Union[Supply, None]:
    return Supply.objects.filter(pk=supply_id).first()


def create_supply(model_form: forms.ModelForm, inserted_by: User) -> Supply:
    supply = model_form.save(commit=False)
    supply = _fill_meta_fields(supply, inserted_by=inserted_by)
    supply.save()
    return supply


def update_supply(
    model_form: forms.ModelForm, updated_by: User = None, updated_at: dt.datetime = None
) -> Supply:
    supply = model_form.save()
    supply = _fill_meta_fields(
        supply, supply.inserted_by, updated_by=updated_by, updated_at=updated_at
    )
    supply.save()
    return supply


def get_supplycontent_itmes(supply: Supply) -> List[SupplyContent]:
    return SupplyContent.objects.filter(supply=supply).all()


def count_supplycontent_itmes(supply: Supply) -> List[SupplyContent]:
    return get_supplycontent_itmes(supply).count()


def update_supplycontent(supply: Supply, content_formset) -> Supply:
    content_formset.save()
    supply.num = count_supplycontent_itmes(supply)
    supply.save()
    return supply
