from django.urls import path
from . import views
from .views import SuaThongtinView, SuaProfileView, ThemProfileView, PasswordChangeView as PW
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('thongtin/', views.thongtin, name='thongtin'),
    path('thongtin/<int:pk>/sua', SuaThongtinView.as_view(), name='suathongtin'),
    path('thongtin/<int:pk>/suaprofile', SuaProfileView.as_view(), name='suaprofile'),
    path('thongtin/<int:pk>/themprofile', ThemProfileView.as_view(), name='themprofile'),
    path('thongtin/password/', PW.as_view(template_name='quanlyxacthuc/changepassword.html'), name='changepassword')
]
