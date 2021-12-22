from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.supply_main), name='supply_main'),
    path('new', login_required(views.supply_new), name='supply_new'),
    path('receiving', login_required(views.receiving_main), name='receiving_main'),
]
