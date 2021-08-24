import datetime as dt

from urllib.parse import urlencode
from django.db.models.query import QuerySet
from django.urls import reverse

from django.http import request
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext

from .models import Country, Employee, EmployeeRole, Organization, Project
from .forms import (LeadscientistForm, OrganizationForm, ProjectForm,
                    EmployeeForm, OrganizationFilter, ProjectFilter)


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


def _extract_countries(form):
    ids = dict(form.data)['countries']
    return [int(id) for id in ids]


@permission_required('organizations.add_organization', raise_exception=True)
def organization_new(request):
    if request.method == "POST":
        form = OrganizationForm(request.user, request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.inserted_by = request.user
            org.updated_by = request.user
            org.save()
            countries = _extract_countries(form)
            org.countries.add(*countries)
            org.save()
            return redirect('organization_detail', pk=org.pk)
    else:
        form = OrganizationForm(request.user)
    return render(request, 'organizations/organization_new.html', {'form': form})


@permission_required('organizations.edit_organization', raise_exception=True)
def organization_edit(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        form = OrganizationForm(request.user, request.POST, instance=org)
        if form.is_valid():
            org = form.save(commit=False)
            org.updated_by = request.user
            for country in org.countries.all():
                org.countries.remove(country)
            countries = _extract_countries(form)
            org.countries.add(*countries)
            org.updated_at = dt.datetime.now()
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


def _get_leadscientist(fields: dict) -> Employee:
    emp, created = Employee.objects.get_or_create(**fields)
    emp.save()
    return emp

@permission_required('organizations.add_project', raise_exception=True)
def project_new(request):
    if request.method == "POST":
        proj_form = ProjectForm(request.user, request.POST)
        emp_form = LeadscientistForm(request.POST)
        emp_role = EmployeeRole.objects.filter(
            name='Ведущий научный сотрудник').first()
        duplicate_error = 'Сотрудник с такими значениями полей Имя, Фамилия и Ученная степень уже существует.'
        if proj_form.is_valid() and (emp_form.is_valid() or duplicate_error in emp_form.errors['__all__']):
            proj = proj_form.save(commit=False)
            emp_fields = emp_form.cleaned_data
            emp_fields.update({
                'updated_by': request.user,
                'inserted_by': request.user,
                'organization': proj.organization,
                'role': emp_role
            })
            emp = _get_leadscientist(emp_fields)
            proj.lead_scientist = emp
            proj.inserted_by = request.user
            proj.updated_by = request.user
            proj.save()

            return redirect('project_detail', pk=proj.pk)
    else:
        proj_form = ProjectForm(request.user,
            initial={'organization':request.GET.get('organization')})
        emp_form = LeadscientistForm()
    return render(request, 'organizations/project_new.html',
                  {'project_form': proj_form, 'scientist_form': emp_form})


@permission_required('organizations.edit_project', raise_exception=True)
def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST, instance=proj)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.updated_by = request.user
            proj.updated_at = dt.datetime.now()
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


@permission_required('organizations.add_employee', raise_exception=True)
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


@permission_required('organizations.edit_employee', raise_exception=True)
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.updated_by = request.user
            emp.updated_at = dt.datetime.now()
            emp.save()
            return redirect('employee_detail', pk=emp.pk)
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'organizations/employee_edit.html', {'form': form})


def main_page(request):
    newest = Organization.objects.order_by('-inserted_at')[:10]
    return render(request, 'organizations/main.html', {'organizations': newest})


def handler404(request, *args, **kwargs):
    data = {'code': 404, 'message': 'Страница не найдена'}
    response = render(request, 'error.html', data)
    return response


def handler403(request, *args, **kwargs):
    data = {'code': 403,
            'message': 'У вас недостаточно прав для просмотра данной страницы'}
    response = render(request, 'error.html', data)
    return response


def handler500(request, *args, **kwargs):
    data = {'code': 500, 'message': 'Страница не найдена'}
    response = render(request, 'error.html', data)
    return response
