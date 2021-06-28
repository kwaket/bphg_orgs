from .models import Organization


def get_organizations():
    return Organization.objects.all()


def add_organization(author):
    organization = Organization.objects.create(
        author=author
    )
    organization.save()
    return organization
