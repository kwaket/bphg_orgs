from users.forms import UserCreateFrom
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator


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
