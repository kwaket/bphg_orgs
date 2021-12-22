from typing import Union
import datetime as dt

from django.shortcuts import get_object_or_404

from .models import CompanyBranch, Source, City, Supply
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
