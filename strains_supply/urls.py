from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.supply_main), name='supply_main'),
    path('new', login_required(views.choose_sourse), name='supply_new'),
    path('new/source', login_required(views.choose_sourse), name='choose_source'),
    path('new/dest', login_required(views.choose_dest), name='choose_dest'),
    path('new/suggesting_data', login_required(views.add_suggesting_data),
        name='add_suggesting_data'),
    path('new/confirm', login_required(views.confirm_supply_creating),
        name='confirm_supply_creating'),
    path('supply/<int:pk>/receiving/steps/<int:step>', login_required(views.receive_supply),
        name='receive_supply'),
    path('supply/<int:pk>', login_required(views.supply_detail),
        name='supply_detail'),
    path('supply/<int:pk>/edit/steps/<int:step>', login_required(views.supply_edit),
        name='supply_edit')
]
