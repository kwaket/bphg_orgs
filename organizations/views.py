import organizations
from django.shortcuts import render
from .models import Organization


def organization_list(request):
    organizations_list = Organization.objects.all().order_by('-id')[:100]
    return render(request, 'organizations/organization_list.html',
        {'organizations': organizations_list})
