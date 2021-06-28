import organizations
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Organization
from .forms import OrganizationForm


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


def organization_new(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.inserted_by = request.user
            org.save()
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/organization_new.html', {'form': form})


def organization_edit(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save(commit=False)
            # org.updated_by = request.user
            org.save()
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm(instance=org)
    return render(request, 'organizations/organization_edit.html', {'form': form})

def project_list(request):
    pass


def main_page(request):
    newest = Organization.objects.order_by('-inserted_at')[:10]
    return render(request, 'organizations/main.html', {'organizations': newest})
