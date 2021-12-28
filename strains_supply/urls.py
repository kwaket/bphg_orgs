from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.supply_main), name='supply_main'),
    path('new', login_required(views.supply_new), name='supply_new'),
    path('supply/<int:pk>/receiving/steps/<int:step>', login_required(views.receive_supply),
        name='receive_supply'),
    path('supply/<int:pk>', login_required(views.supply_detail),
        name='supply_detail')
]
