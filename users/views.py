from django.urls.base import is_valid_path, translate_url
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.contrib import messages

from users.forms import ProfileForm, UserForm


@permission_required('users.edit_user', raise_exception=True)
def user_list(request):
    page_num = request.GET.get('page')
    order_by = request.GET.get('order_by') or 'username'
    queryset = User.objects.all().order_by(order_by)

    paginator = Paginator(queryset, 25)
    page = paginator.get_page(page_num)
    url_new = reverse('user_new', args=[], kwargs={})
    args = {
        'page': page,
        'current_page': page_num,
        'current_order': order_by,
        'url_new': url_new
    }
    return render(request, 'users/user_list.html', args)


@permission_required('user.add_user')
def profile_new(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Пользователь создан')
            return redirect('user_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'users/profile_new.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@permission_required('user.edit_user')
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            group = get_object_or_404(Group, pk=int(user_form.data['group']))
            user.groups.clear()
            user.groups.add(group)
            user.save()
            profile_form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    args = {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_edit.html', args)



@permission_required('users.view_user', raise_exception=True)
def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    url_new = reverse('user_edit', args=[], kwargs={'pk': user.pk})
    args = {
        'obj': user,
        'url_new': url_new,
        'page_name': 'Пользователь'
        }
    return render(request, 'users/profile_detail.html', args)
