from django.shortcuts import render
from .models import Group


def home_page(request):
    groups = Group.objects.all()
    return render(request, 'base/home.html', {"groups": groups})


def group_page(request, pk):
    groups = Group.objects.all()
    selected_group = {}
    participants = []
    for group in groups:
        if group.id == pk:
            selected_group = group
    return render(request, 'base/group_page.html', {'group': selected_group})
