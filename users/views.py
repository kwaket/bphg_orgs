from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User


def user_list(request):
    if not request.user.groups.filter(name="Модераторы").exists():
        redirect
    users = User.objects.all()
    url_new = reverse('user_new', args=[], kwargs={})
    return render(request, 'users/user_list.html',
        {'users': users, 'url_new': url_new})


def user_new(request):
    return render(request, 'users/user_new.html')


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})


def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_edit.html', {'user': user})
