from django.contrib import admin
from .models import User, Group, Time


admin.site.register(User)
admin.site.register(Group)
admin.site.register(Time)
