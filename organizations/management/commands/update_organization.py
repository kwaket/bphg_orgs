import random
from django.core.management.base import BaseCommand, CommandError
from organizations.models import Organization

from ._utils import is_dark_theme

class Command(BaseCommand):
    help = 'Update organization card theme'

    def handle(self, *args, **options):
        orgs = Organization.objects.all()
        for org in orgs:
            if org.image:
                org.theme_is_dark = is_dark_theme(org.image)
            elif not org.image and org.theme_is_dark is not None:
                continue
            else:
                org.theme_is_dark = bool(random.randint(0, 1))
            org.save()

