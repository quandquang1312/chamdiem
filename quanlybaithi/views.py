from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Baithi
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView

from .forms import BaithiForm

# Create your views here.

def danhsachbaithi(request):
    baithis = Baithi.objects.all()
    return render(request, 'quanlybaithi/danhsachbaithi.html', {'baithis': baithis})

def chitietbaithi(request, id):
    baithi = Baithi.objects.get(id=id)
    return render(request, 'quanlybaithi/chitietbaithi.html', {'baithi': baithi})

class TaoBaithiView(CreateView):
    model = Baithi
    form_class = BaithiForm
    template_name = 'quanlybaithi/taobaithi.html'

class XoaBaithiView(DeleteView):
    model = Baithi
    template_name = 'quanlybaithi/xoabaithi.html'
    success_url = reverse_lazy('danhsachbaithi')

class SuaBaithiView(UpdateView):
    model = Baithi
    form_class = BaithiForm
    template_name = 'quanlybaithi/suabaithi.html'
    # fields = ('ten',)


