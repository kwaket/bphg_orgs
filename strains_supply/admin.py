from django.contrib import admin

from .models import Supply, SupplyContent, Strain, Source, City, CompanyBranch

admin.site.register([Supply, SupplyContent, Strain, Source, City, CompanyBranch])
