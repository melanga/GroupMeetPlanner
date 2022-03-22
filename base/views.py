from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ModifiedUserCreationForm, GroupForm
from .models import Group, Time, User


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
    if request.method == "POST":
        time = Time.objects.create(
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            user=request.user,
            group=group
        )
        group.members.add(request.user)
        return redirect('group', pk=group.id)
    return render(request, 'base/group_page.html', {'group': group, 'time_slots': time_slots})


@login_required(login_url='login')
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
    group.delete()
    return redirect('home')


@login_required(login_url='login')
def delete_time(request, pk):
    time = Time.objects.get(id=pk)
    time.delete()
    return redirect('group', pk=time.group.id)


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


def logout_user(request):
    logout(request)
    return redirect('home')
