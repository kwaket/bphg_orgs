from django.urls import path
from . import views
import organizations


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('organizations', views.organization_list, name='organization_list'),
    path('organizations/<int:pk>/', views.organization_detail, name='organization_detail'),
    path('organizations/new/', views.organization_new, name='organization_new'),
    path('organizations/<int:pk>/edit', views.organization_edit, name='organization_edit'),
    path('projects', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.organization_detail, name='project_detail'),
    path('projects/new/', views.organization_new, name='project_new'),
    path('projects/<int:pk>/edit', views.organization_edit, name='project_edit'),
]
