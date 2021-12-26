from django.urls import path, include

from . import views
from .views import TaoBaithiView, XoaBaithiView, SuaBaithiView
from .views import TaoBailamView, SuaBailamView, XoaBailamView
from .views import TaoBodapan

urlpatterns = [
    path('danhsachbaithi/', views.danhsachbaithi, name='danhsachbaithi'),
    path('danhsachbaithi/<int:id>', views.chitietbaithi, name='chitietbaithi'),
    path('taobaithi/', TaoBaithiView.as_view(), name='taobaithi'),
    path('danhsachbaithi/<int:pk>/delete', XoaBaithiView.as_view(), name='xoabaithi'),
    path('danhsachbaithi/<int:pk>/edit', SuaBaithiView.as_view(), name='suabaithi'),
    path('danhsachbaithi/<int:pk>/taobailam', TaoBailamView.as_view(), name='taobailam'),
    path('danhsachbaithi/<int:id>/chitietbailam', views.chitietbailam, name='chitietbailam'),
    path('danhsachbaithi/chitietbailam/<int:baithi_id>/<int:bailam_id>', views.chamdiem, name='chamdiem'),
    path('danhsachbaithi/chitietbailam/<int:pk>/edit', SuaBailamView.as_view(), name='suabailam'),
    path('danhsachbaithi/chitietbailam/<int:pk>/delete', XoaBailamView.as_view(), name='xoabailam'),
    path('danhsachbaithi/<int:pk>/capnhatsocau', views.capnhatsocau, name='capnhatsocau'),
    path('danhsachbaithi/getsbd/<int:bailam_id>', views.laysbd, name='laysbd'),
    path('danhsachbaithi/<int:bailam_id>/taodapan', TaoBodapan.as_view(), name='taodapan'),
    path('danhsaschbaithi/chitietbode/<int:baithi_id>', views.chitietbode, name='chitietbode')
]