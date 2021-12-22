from django.urls import path
from . import views
from .views import SuaThongtinView, SuaProfileView, ThemProfileView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('thongtin/', views.thongtin, name='thongtin'),
    path('thongtin/<int:pk>/sua', SuaThongtinView.as_view(), name='suathongtin'),
    path('thongtin/<int:pk>/suaprofile', SuaProfileView.as_view(), name='suaprofile'),
    path('thongtin/<int:pk>/themprofile', ThemProfileView.as_view(), name='themprofile')
]
