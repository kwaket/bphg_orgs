from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from strains_supply.models import CompanyBranch


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.PROTECT,
                                      null=True, blank=True, verbose_name='Филиал')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
