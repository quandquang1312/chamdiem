from django.contrib import auth
from django.contrib.auth import authenticate, login as l, logout as lo
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView

from quanlyxacthuc.forms import CreateUserForm, ProfileForm, UserForm
from quanlyxacthuc.models import Profile
from django.urls import reverse_lazy

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            l(request, user)
            return render(request, 'core/home.html')
        else:
            pass
    return render(request, 'quanlyxacthuc/login.html')

def logout(request):
    lo(request)
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return HttpResponse('Failed')
    form = CreateUserForm
    return render(request, 'quanlyxacthuc/register.html', {'form': form}) 

def thongtin(request):
    return render(request, 'quanlyxacthuc/thongtin.html')

class SuaThongtinView(UpdateView):
    model = User
    template_name = 'quanlyxacthuc/suathongtin.html'
    form_class = UserForm

class SuaProfileView(UpdateView):
    model = Profile
    template_name = 'quanlyxacthuc/suaprofile.html'
    form_class = ProfileForm

class ThemProfileView(CreateView):
    model = Profile
    template_name = 'quanlyxacthuc/themthongtin.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
    