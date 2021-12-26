from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sdt', 'hoten', 'user')

        widgets = {
            'sdt': forms.TextInput(attrs={'class': 'label-form'}),
            'hoten': forms.TextInput(attrs={'class': 'label-form'}),
            'user': forms.TextInput(attrs={'class': 'label-form', 'id': 'author', 'type': 'hidden'}),
        }

        labels = {
            'sdt': 'Số điện thoại',
            'hoten': 'Mô tả'
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'label-form'}),
            'last_name': forms.TextInput(attrs={'class': 'label-form'}),
            'email': forms.TextInput(attrs={'class': 'label-form'})
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'label-form', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'label-form', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'label-form', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_pasfsword', 'new_password1', 'new_password2')

        labels = {
            'old_password': 'Mật khẩu cũ'
        }
