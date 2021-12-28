from typing import List, Union
import datetime as dt

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Q, Sum

from .models import BacteriaType, CompanyBranch, Source, City, Strain, Supply, SupplyContent
from django.contrib.auth.models import User
from . import utils


def create_city(name: str, inserted_by: User) -> City:
    city = City.objects.create(name=name, inserted_by=inserted_by,
                               updated_by=inserted_by)
    city.save()
    return city


def get_or_create_city(inserted_by: User, source_id: int=None, name: str=None) -> City:
    if source_id:
        return get_object_or_404(City, pk=source_id)
    if name:
        alias = utils.get_alias(name)
        city = City.objects.filter(alias=alias).first()
        if city:
            return city
    return create_city(name, inserted_by=inserted_by)


def get_source(name: str, city: City) -> Source:
    return Source.objects.filter(name=name, city=city.id).first()


def get_source_by_id(source_id: int) -> Source:
    return get_object_or_404(Source, pk=source_id)


def create_source(name: str, city: City) -> Source:
    source = Source.objects.create(name=name, city=city)
    source.save()
    return source


def get_or_create_source(inserted_by: User, source_id: int, name: str=None, city: str=None) -> Source:
    if source_id:
        return get_source_by_id(source_id)
    city = get_or_create_city(name=city, inserted_by=inserted_by)
    source = get_source(name, city)
    if not source:
        source = create_source(name, city)
    return source


def get_dest_by_id(id: int) -> CompanyBranch:
    return get_object_or_404(CompanyBranch, pk=id)


def create_dest(name: str, inserted_by: User) -> CompanyBranch:
    branch = CompanyBranch.objects.create(name=name,
                                          inserted_by=inserted_by,
                                          updated_by=inserted_by)
    branch.save()
    return branch


def get_or_create_dest(dest_id: int, name: str,
                       inserted_by: User=None) -> CompanyBranch:
    if dest_id:
        dest = CompanyBranch.objects.filter(pk=dest_id).first()
        if dest:
            return dest

    alias = utils.get_alias(name)
    dest = CompanyBranch.objects.filter(alias=alias).first()
    if not dest:
        dest = create_dest(name, inserted_by=inserted_by)
    return dest

def get_supply_or_404(pk: int):
    return get_object_or_404(Supply, pk=pk)

def create_supply(inserted_by: User, source: Source, dest: CompanyBranch,
                  suggested_sent_date: dt.date=None, suggested_num: int=None) -> Supply:
    supply = Supply.objects.create(
        source=source,
        dest=dest,
        suggested_sent_date=suggested_sent_date,
        suggested_num=suggested_num,
        inserted_by=inserted_by,
        updated_by=inserted_by
    )
    supply.save()
    return supply


def get_companybranch(user: User) -> Union[CompanyBranch, None]:
    """Function return CompanyBranch related to user."""
    if user.is_anonymous:
        return None
    return user.profile.company_branch


def get_supplylist_for_user(user: User, limit=10) -> Union[QuerySet, list]:
    """Function return list of supply related to user's company branch"""
    company_branch = get_companybranch(user)
    is_moderator = is_supply_moderator(user)
    if is_moderator:
        supply_list = Supply.objects.filter(Q(received_at=None) | Q(num=None))\
            .all().order_by('-inserted_at')[:limit]
        return supply_list
    if company_branch:
        supply_list = Supply.objects.filter(dest=company_branch)\
            .filter(Q(received_at=None) | Q(num=None))\
            .all().order_by('-inserted_at')[:limit]
        return supply_list
    return []

def get_newest_supply_for_user(user: User, limit=25) -> Union[QuerySet, list]:
    """Function return list of newest supply.

    List sorted by:
    - not received (field num is empty)
    - inserted date (inserted_at)
    """
    company_branch = get_companybranch(user)
    is_moderator = is_supply_moderator(user)
    if is_moderator:
        supply_list = Supply.objects.all().order_by('-num', '-inserted_at')[:limit]
        return supply_list
    if company_branch:
        supply_list = Supply.objects.filter(dest=company_branch)\
            .all().order_by('-num', '-inserted_at')[:limit]
        return supply_list
    return []


def get_supply(pk: int) -> Supply:
    return get_object_or_404(Supply, pk=pk)


def receive_supply(supply: Supply, user: User, received_at: dt.datetime,
                   sent_at: dt.datetime=None) -> Supply:
    """Function update receiving fields and correct sent_at field if possible"""
    supply.received_at = received_at
    supply.sent_at = sent_at
    supply.updated_at = dt.datetime.now()
    supply.updated_by = user
    supply.save()
    return supply


def get_strain(pk: int) -> Strain:
    return get_object_or_404(Strain, pk=pk)


def update_supplycontent_item(supply: Supply, bacteria_type: BacteriaType,
                            strain: str, delete:str) -> SupplyContent:
    item = SupplyContent.objects.create(supply=supply, bacteria_type=bacteria_type,
                                        strain=strain)
    return item


def unpack_supply(content: List[dict]) -> Supply:
    for item in content:
        item['delete'] = item.pop('DELETE')
        if item.get('bacteria_type') and item.get('delete'):
            continue
        update_supplycontent_item(**item)
    supply = content[0]['supply']
    total = SupplyContent.objects.filter(supply=supply).count()
    supply.num = total
    supply.save()
    return supply


def add_remark_to_supply(supply: Supply, remark:str) -> Supply:
    supply.received_remark = remark
    supply.save()
    return supply

def count_unreceived_supply(user: User) -> int:
    company_branch = get_companybranch(user)
    if company_branch:
        return Supply.objects.filter(dest=company_branch, num=None).all().count()
    if is_supply_moderator(user):
        return Supply.objects.filter(num=None).all().count()
    return 0


# permissions
def is_supply_moderator(user: User) -> bool:
    gr = user.groups.filter(name='Поставки (Администратор)').first()
    if gr:
        return True
    return False
