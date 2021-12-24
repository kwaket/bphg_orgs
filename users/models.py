from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from strains_supply.models import CompanyBranch


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.PROTECT,
                                      null=True, blank=True, verbose_name='Филиал')

    def __str__(self):
        if self.company_branch:
            return r'{self.user.name}, {self.company_branch.name}'
        return self.user.name

