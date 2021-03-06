from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .time_operations import check_time_validity, get_available_times
from .forms import ModifiedUserCreationForm, GroupForm, UserForm
from .models import Group, Time, User

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


def home_page(request):
    groups = {}
    if request.user.is_authenticated:
        groups = Group.objects.filter(
            Q(members=request.user)
        )
    return render(request, 'base/home.html', {"groups": groups})


def group_page(request, pk):
    group = Group.objects.get(id=pk)
    time_slots = group.time_set.all()
    time_sets = []
    for member in group.members.all():
        each_member_time_set = time_slots.filter(user_id=member.id)
        if each_member_time_set.count() != 0:
            time_sets.append(each_member_time_set)
    available_times = []
    if time_sets:
        available_times = get_available_times(time_sets)
    q = request.GET.get('q')
    user_search = {}
    if q is not None:
        user_search = User.objects.filter(username__contains=q)
    if request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if check_time_validity(start_time, end_time):
            time = Time.objects.create(
                start_time=start_time,
                end_time=end_time,
                user=request.user,
                group=group
            )
            group.members.add(request.user)
            return redirect('group', pk=group.id)
        else:
            return redirect('group', pk=group.id)

    return render(request, 'base/group_page.html', {
        'group': group,
        'time_slots': time_slots,
        'users': user_search,
        'available_times': available_times,
    })


def add_member(request, uid, gid):
    user = User.objects.get(id=uid)
    group = Group.objects.get(id=gid)
    group.members.add(user)
    return redirect('group', pk=gid)


def remove_member(request, uid, gid):
    user = User.objects.get(id=uid)
    group = Group.objects.get(id=gid)
    group.members.remove(user)
    return redirect('group', pk=gid)


def leave_group(request, gid):
    group = Group.objects.get(id=gid)
    group.members.remove(request.user)
    return redirect('home')


@login_required(login_url='login-page')
def group_creation_page(request):
    form = GroupForm
    if request.method == "POST":
        # Group.objects.create(
        #     leader=request.user,
        #     name=request.POST.get('name'),
        #     description=request.POST.get('description')
        # )
        created_group = GroupForm(request.POST).save(commit=False)
        created_group.leader = request.user
        created_group.save()
        created_group.members.add(request.user)
        return redirect('group', pk=created_group.id)
    return render(request, 'base/group_creation_page.html', {'group_form': form})


@login_required(login_url='login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        group.delete()
        return redirect('home')
    return render(request, 'base/confirm_delete.html', {'obj': group})


def update_group(request, gid):
    group = Group.objects.get(id=gid)
    group_form = GroupForm(instance=group)
    if request.method == "POST":
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.save()
        return redirect('group', pk=group.id)
    return render(request, 'base/update_group.html', {'group_form': group_form})


@login_required(login_url='login')
def delete_time(request, pk):
    time = Time.objects.get(id=pk)
    if request.method == "POST":
        time.delete()
        return redirect('group', pk=time.group.id)
    return render(request, 'base/confirm_delete.html', {'obj': time})


def update_time(request, pk):
    time = Time.objects.get(id=pk)
    if request.method == "POST":
        time.start_time = request.POST.get("start_time")
        time.end_time = request.POST.get("end_time")
        if check_time_validity(time.start_time, time.end_time):
            time.save()
            return redirect('group', time.group.id)
        else:
            print("enter valid time")
            return redirect('update_time', time.id)
    return render(request, 'base/update_time.html', {'time': time})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "enter correct password")

    return render(request, 'base/login.html')


def register_user(request):
    form = ModifiedUserCreationForm()
    if request.method == "POST":
        form = ModifiedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/register.html', {'register_form': form})


def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/update_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'base/password_change.html'
