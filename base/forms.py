from django.forms import ModelForm
from .models import User, Group
from django.contrib.auth.forms import UserCreationForm


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['members', 'leader']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'name', 'username', 'email', 'bio']


class ModifiedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
