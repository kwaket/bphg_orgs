import random
from django.core.management.base import BaseCommand, CommandError
from organizations.models import Organization

from ._utils import download_file_to_media

class Command(BaseCommand):
    help = 'Update organization card theme'

    def handle(self, *args, **options):
        orgs = Organization.objects.all()
        for org in orgs:
            if org.image and not org.image.startswith('/'):
                org.image = download_file_to_media(org.image)
                org.save()
            if org.logo and not org.logo.startswith('/'):
                org.logo = download_file_to_media(org.logo)
                org.save()
