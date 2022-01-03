from typing import Union

from django.contrib.auth.models import User

from strains_supply.models import CompanyBranch


def is_moderator(user: User) -> bool:
    gr = user.groups.filter(name='Поставки (Администратор)').first()
    if gr:
        return True
    return False


def get_user_companybranch(user: User) -> Union[CompanyBranch, None]:
    """Function return CompanyBranch related to user."""
    if user.is_anonymous:
        return None
    return user.profile.company_branch


