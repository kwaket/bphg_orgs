import organizations
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Organization


def organization_list(request):
    org_list = Organization.objects.all()
    paginator = Paginator(org_list, 25)
    page = request.GET.get('page')
    orgs = paginator.get_page(page)
    return render(request, 'organizations/organization_list.html',
        {'organizations': orgs})


def organization_detail(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/organization_detail.html',
        {'organization': org})


def project_list(request):
    pass


def main_page(request):
    newest = Organization.objects.order_by('-inserted_at')[:10]
    return render(request, 'organizations/main.html', {'organizations': newest})
