from django.urls import path
from . import views
import organizations


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('organizations', views.organization_list, name='organization_list'),
    path('projects', views.project_list, name='project_list')
]
