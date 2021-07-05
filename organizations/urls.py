from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.main_page), name='main_page'),
    path('organizations', login_required(views.organization_list),
         name='organization_list'),
    path('organizations/<int:pk>/', login_required(views.organization_detail),
         name='organization_detail'),
    path('organizations/new/', login_required(views.organization_new),
         name='organization_new'),
    path('organizations/<int:pk>/edit', login_required(views.organization_edit),
         name='organization_edit'),
    path('projects', login_required(views.project_list),
         name='project_list'),
    path('projects/<int:pk>/', login_required(views.project_detail),
         name='project_detail'),
    path('projects/new/', login_required(views.project_new),
         name='project_new'),
    path('projects/<int:pk>/edit', login_required(views.project_edit),
         name='project_edit'),
]
