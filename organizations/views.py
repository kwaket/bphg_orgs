from urllib.parse import urlencode
from django.db.models.query import QuerySet
from django.urls import reverse

from django.http import request
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Country, Employee, Organization, Project
from .forms import (OrganizationForm, ProjectForm, EmployeeForm,
                    OrganizationFilter, ProjectFilter)


def _delete_params(params: dict, exclude: list) -> dict:
    for key in exclude:
        if key in params:
            del params[key]
    return params


def organization_list(request):
    mode = request.GET.get('mode', 'list')
    if mode == 'by_country':
        query = Country.objects.all().order_by('name').query
        query.group_by = ['name']
        queryset = QuerySet(query=query, model=Country)
        args = {'countries': queryset, 'mode': mode}
        return render(request, 'organizations/organization_list.html', args)
    else:
        page = request.GET.get('page')
        order_by = request.GET.get('order_by') or 'inserted_at'
        queryset = Organization.objects.all().order_by(order_by)
        filter_orgs = OrganizationFilter(request.GET, queryset=queryset)
        filter_fields = _delete_params(request.GET.copy(),
                                    exclude=['page', 'order_by'])
        paginator = Paginator(filter_orgs.qs, 25)
        orgs_page = paginator.get_page(page)
        args = {
            'organizations_page': orgs_page,
            'filter': filter_orgs,
            'filter_fields': urlencode(filter_fields),
            'current_page': page,
            'current_order': order_by,
            'mode': mode
        }
        return render(request, 'organizations/organization_list.html', args)


def organization_detail(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/organization_detail.html',
        {'organization': org})


def organization_new(request):
    if request.method == "POST":
        form = OrganizationForm(request.user, request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.inserted_by = request.user
            org.updated_by = request.user
            org.save()
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm(request.user)
    return render(request, 'organizations/organization_new.html', {'form': form})


def organization_edit(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        form = OrganizationForm(request.user, request.POST, instance=org)
        if form.is_valid():
            org = form.save(commit=False)
            org.updated_by = request.user
            org.save()
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm(request.user, instance=org)
    return render(request, 'organizations/organization_edit.html', {'form': form})


def project_list(request):
    page = request.GET.get('page')
    order_by = request.GET.get('order_by') or 'inserted_at'
    queryset = Project.objects.all().order_by(order_by)
    filter_projs = ProjectFilter(request.GET, queryset=queryset)
    filter_fields = _delete_params(request.GET.copy(),
                                   exclude=['page', 'order_by'])
    paginator = Paginator(filter_projs.qs, 25)
    projs_page = paginator.get_page(page)
    args = {
        'projects_page': projs_page,
        'filter': filter_projs,
        'filter_fields': urlencode(filter_fields),
        'current_page': page,
        'current_order': order_by
    }
    return render(request, 'organizations/projects_list.html', args)


def project_detail(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    return render(request, 'organizations/project_detail.html',
        {'project': proj})


def project_new(request):
    if request.method == "POST":
        form = ProjectForm(request.user, request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.inserted_by = request.user
            proj.updated_by = request.user
            proj.save()
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm(request.user, initial={'organization':request.GET.get('organization')})
    return render(request, 'organizations/project_new.html', {'form': form})


def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST, instance=proj)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.updated_by = request.user
            proj.save()
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm(request.user, instance=proj,
            initial={'lead_scientist': proj.lead_scientist.name,
                     'application_scope': proj.application_scope.name})
    return render(request, 'organizations/project_edit.html', {'form': form})


def employee_list(request):
    page = request.GET.get('page')
    order_by = request.GET.get('order_by') or 'inserted_at'
    queryset = Employee.objects.all().order_by(order_by)
    paginator = Paginator(queryset, 25)
    emps_page = paginator.get_page(page)
    url_new = reverse('employee_new', args=[], kwargs={})
    args = {
        'page': emps_page,
        'current_page': page,
        'current_order': order_by,
        'button_url': url_new,
    }
    return render(request, 'organizations/employee_list.html', args)


def employee_new(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.inserted_by = request.user
            emp.updated_by = request.user
            emp.save()
            return redirect('employee_detail', pk=emp.pk)
    else:
        form = EmployeeForm()
    return render(request, 'organizations/employee_new.html', {'form': form})


def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    url = reverse('employee_edit', args=[], kwargs={'pk': emp.pk})
    args = {
        'obj': emp,
        'page_name': emp.get_full_name(),
        'button_url': url
    }
    return render(request, 'organizations/employee_detail.html', args)


def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.updated_by = request.user
            emp.save()
            return redirect('employee_edit', pk=emp.pk)
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'organizations/employee_edit.html', {'form': form})



def main_page(request):
    newest = Organization.objects.order_by('-inserted_at')[:10]
    return render(request, 'organizations/main.html', {'organizations': newest})
