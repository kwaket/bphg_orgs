from django.urls import path
from . import views


urlpatterns = [
    path('', views.organization_list, name='organization_list')
]
