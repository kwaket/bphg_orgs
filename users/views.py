from users.forms import UserCreateFrom
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
    if request.method == "POST":
        form = UserCreateFrom(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserCreateFrom()
    return render(request, 'users/user_new.html', {'form': form})


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})


def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_edit.html', {'user': user})
