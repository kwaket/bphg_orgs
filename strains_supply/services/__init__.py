from django.contrib.auth.models import User
from django.http import request
from django import forms

from strains_supply.models import CompanyBranch, Source, Supply

from . import crud


def choose_supply_source(source_id: int=None, name: str=None, city: str=None,
                         inserted_by: User=None) -> Source:
    return crud.get_or_create_source(source_id=source_id, name=name, city=city,
                                     inserted_by=inserted_by)


def choose_supply_dest(dest_id: int=None, name: str=None, city: str=None,
                       inserted_by: User=None) -> CompanyBranch:
    if dest_id:
        return crud.get_dest(dest_id)
    return crud.get_or_create_dest(name, inserted_by)


def add_supply(model_form: forms.ModelForm, inserted_by: User) -> Supply:
    supply = crud.create_supply(model_form, inserted_by)
    return supply


def get_source(source_id: int) -> Source:
    return crud.get_source(source_id=source_id)


def get_dest(dest_id: int) -> CompanyBranch:
    return crud.get_dest(dest_id=dest_id)
