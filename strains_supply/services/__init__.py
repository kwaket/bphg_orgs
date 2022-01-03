from django.contrib.auth.models import User
from django import forms

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
    return crud.get_or_create_source(
        source_id=source_id, name=name, city=city, inserted_by=inserted_by
    )


def choose_supply_dest(
    dest_id: int = None, name: str = None, city: str = None, inserted_by: User = None
) -> CompanyBranch:
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
