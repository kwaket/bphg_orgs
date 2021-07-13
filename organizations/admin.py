from django.contrib import admin
from .models import Organization, Country, EmployeeRole, Employee,\
    ApplicationScope, Project, Progress

admin.site.register([Organization, Country, EmployeeRole, Employee,
    ApplicationScope, Project, Progress])
