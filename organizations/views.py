from urllib.parse import urlencode

from django.http import request
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Organization, Project
from .forms import (OrganizationForm, ProjectForm, OrganizationFilter,
                    ProjectFilter)


def organization_list(request):
    page = request.GET.get('page')
    filter_fields = request.GET
    filter_orgs = OrganizationFilter(request.GET,
                                     queryset=Organization.objects.all())
    filter_fields = {k: v for k, v in filter_fields.items() if k in filter_orgs.filters}
    paginator = Paginator(filter_orgs.qs, 25)
    orgs_page = paginator.get_page(page)
    args = {
        'organizations_page': orgs_page,
        'filter': filter_orgs,
        'filter_fields': urlencode(filter_fields)
    }
    return render(request, 'organizations/organization_list.html', args)


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
    page = request.GET.get('page')
    filter_fields = request.GET
    filter_projs = ProjectFilter(request.GET,
                                 queryset=Project.objects.all())
    filter_fields = {k: v for k, v in filter_fields.items() if k in filter_projs.filters}
    paginator = Paginator(filter_projs.qs, 25)
    projs_page = paginator.get_page(page)
    args = {
        'projects_page': projs_page,
        'filter': filter_projs,
        'filter_fields': urlencode(filter_fields)
    }
    return render(request, 'organizations/projects_list.html', args)


def project_detail(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    return render(request, 'organizations/project_detail.html',
        {'project': proj})


def project_new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.inserted_by = request.user
            proj.save()
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm(initial={'organization':request.GET.get('organization')})
    return render(request, 'organizations/project_new.html', {'form': form})


def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=Project)
        if form.is_valid():
            proj = form.save(commit=False)
            # org.updated_by = request.user
            proj.save()
            return redirect('organiztions/project_detail.html', pk=proj.pk)
    else:
        form = ProjectForm(instance=proj)
    return render(request, 'organizations/project_edit.html', {'form': form})


def main_page(request):
    newest = Organization.objects.order_by('-inserted_at')[:10]
    return render(request, 'organizations/main.html', {'organizations': newest})
