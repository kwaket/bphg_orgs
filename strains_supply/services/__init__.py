import datetime as dt
from django.http import Http404
from django.contrib.auth.models import User
from django import forms
from django.forms import modelformset_factory

from strains_supply.models import CompanyBranch, Source, Supply

from . import crud
from . import permissions


def get_newest_supply_for_user(user: User, limit: int = 10):
    """Function return list of newest supply for user.

    List sorted by:
    - not received (field received_at is empty)
    - sent date (sent_at)
    - suggested sent date (suggested_sent_date)
    - recieved date (received_at)
    """
    company_branch = permissions.get_user_companybranch(user)
    is_moderator = permissions.is_moderator(user)
    if is_moderator:
        supply_list = Supply.objects.order_by(
            "-received_at", "-sent_at", "-suggested_sent_date", "-received_at"
        )[:limit]
        return supply_list
    if company_branch:
        supply_list = Supply.objects.filter(dest=company_branch).order_by(
            "-received_at", "-sent_at", "-suggested_sent_date", "-received_at"
        )[:limit]
        return supply_list
    return Supply.objects.none()


def choose_supply_source(
    source_id: int = None, name: str = None, city: str = None, inserted_by: User = None
) -> Source:
    city = crud.get_or_create_city(name=city, inserted_by=inserted_by)
    return crud.get_or_create_source(
        source_id=source_id, name=name, city=city, inserted_by=inserted_by
    )


def choose_supply_dest(
    dest_id: int = None, name: str = None, city: str = None, inserted_by: User = None
) -> CompanyBranch:
    return crud.get_or_create_dest(dest_id=dest_id, name=name, inserted_by=inserted_by)


def get_source(source_id: int) -> Source:
    return crud.get_source(source_id=source_id)


def get_dest(dest_id: int) -> CompanyBranch:
    return crud.get_dest(dest_id=dest_id)


def get_supply(supply_id: int) -> Supply:
    supply = crud.get_supply(supply_id)
    if supply:
        return supply
    raise Http404


def add_supply(model_form: forms.ModelForm, inserted_by: User) -> Supply:
    supply = crud.create_supply(model_form, inserted_by)
    return supply


def receive_supply(model_form: forms.ModelForm, received_by: User) -> Supply:
    now = dt.datetime.now()
    supply = crud.update_supply(
        model_form=model_form, updated_by=received_by, updated_at=now
    )
    return supply


def unpack_supply(supply: Supply, content_formset: modelformset_factory) -> Supply:
    supply = crud.update_supplycontent(supply=supply, content_formset=content_formset)
    return supply


def edit_supply_content(
    supply: Supply, content_formset: modelformset_factory
) -> Supply:
    supply = crud.update_supplycontent(supply=supply, content_formset=content_formset)
    return supply


def add_supply_remark(model_form: forms.ModelForm) -> Supply:
    supply = model_form.save()
    return supply
