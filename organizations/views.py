import organizations
from django.shortcuts import render
from .models import Organization


def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, 'organizations/organization_list.html',
        {'organizations': organizations})
