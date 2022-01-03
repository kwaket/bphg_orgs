from django import forms
from django.contrib.auth.models import User
from django.db.models import Model

from strains_supply.models import CompanyBranch, Source, City, Supply

from .. import utils


def _fill_meta_fields(model: Model, inserted_by: User, updated_by: User = None):
    model.inserted_by = inserted_by
    model.updated_by = updated_by or inserted_by
    return model


def get_city(city_id: int) -> City:
    return City.objects.get(pk=city_id)


def create_city(name: str, inserted_by: User) -> City:
    alias = utils.get_alias(name)
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
    return create_dest(name, inserted_by)


def create_supply(model_form: forms.ModelForm, inserted_by: User):
    supply = model_form.save(commit=False)
    supply = _fill_meta_fields(supply, inserted_by=inserted_by)
    supply.save()
    return supply
