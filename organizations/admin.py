from django.contrib import admin
from .models import Organization, Country, City, EmployeeRole, Employee,\
    ApplicationScope, Project

admin.site.register([Organization, Country, City, EmployeeRole, Employee,
    ApplicationScope, Project])