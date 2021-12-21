from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.main_page), name='main_page'),
    path('new', login_required(views.supply_new), name='supply_new'),
]
