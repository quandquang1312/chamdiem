from django.urls import path, include

from . import views
from .views import TaoBaithiView, XoaBaithiView, SuaBaithiView

urlpatterns = [
    path('danhsachbaithi/', views.danhsachbaithi, name='danhsachbaithi'),
    path('danhsachbaithi/<int:id>', views.chitietbaithi, name='chitietbaithi'),
    path('taobaithi/', TaoBaithiView.as_view(), name='taobaithi'),
    path('danhsachbaithi/<int:pk>/delete', XoaBaithiView.as_view(), name='xoabaithi'),
    path('danhsachbaithi/<int:pk>/edit', SuaBaithiView.as_view(), name='suabaithi')
]