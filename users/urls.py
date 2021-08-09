from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', login_required(views.user_list), name='user_list'),
    path('new/', login_required(views.user_new), name='user_new'),
    path('<int:pk>/', login_required(views.user_detail), name='user_detail'),
    path('<int:pk>/edit', login_required(views.user_edit), name='user_edit'),
]
