from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse as ht
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Bailam, Baithi, Bodapan
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView

from .forms import BailamForm, BaithiForm

from .mlfunctions import result as diemrs
from .mlfunctions import get_sbd

from .custom_model import BailamSerializer


# Create your views here.

def danhsachbaithi(request):
    baithis = Baithi.objects.all()
    return render(request, 'quanlybaithi/danhsachbaithi.html', {'baithis': baithis})

def chitietbaithi(request, id):
    baithi = Baithi.objects.get(id=id)
    return render(request, 'quanlybaithi/chitietbaithi.html', {'baithi': baithi})

def chitietbailam(request, id):
    baithi = Baithi.objects.get(id=id)
    bailams = Bailam.objects.filter(baithi=baithi)
    return render(request, 'quanlybaithi/chitietbailam.html', {'bailams': bailams})

def chitietbode(request, baithi_id):
    baithi = Baithi.objects.get(id=baithi_id)
    bdapans = Bodapan.objects.filter(baithi=baithi)

    return render(request, 'quanlybaithi/chitietbode.html', {'bdapans': bdapans})

class TaoBaithiView(CreateView):
    model = Baithi
    form_class = BaithiForm
    # fields = '__all__'
    template_name = 'quanlybaithi/taobaithi.html'

class XoaBaithiView(DeleteView):
    model = Baithi
    template_name = 'quanlybaithi/xoabaithi.html'
    success_url = reverse_lazy('danhsachbaithi')

def capnhatsocau(request, pk):
    baithi = Baithi.objects.get(id=pk)
    bt_url = baithi.ketqua.url
    kq = diemrs(bt_url)
    baithi.socau = len(kq)
    baithi.save()
    return HttpResponseRedirect(reverse_lazy('danhsachbaithi'))


def chamdiem(request, baithi_id, bailam_id):
    
    baithi = Baithi.objects.get(id=str(baithi_id))
    bodapan = Bodapan.objects.filter(baithi=baithi)
    bailam = Bailam.objects.get(id=str(bailam_id))

    bl_url = bailam.bai.url

    sbd, md = get_sbd(bl_url)
    return HttpResponse(str(bl_url) + " " + str(sbd) + " " + str(md))
    bda = bodapan.get(bmade=md)
    bt_url = bda.dapan.url

    kq = diemrs(bt_url)
    diem = diemrs(bl_url)
    dung = {k: diem[k] for k in diem if k in kq and diem[k] == kq[k]}
    
    bailam.diem = len(dung)
    
    bailam.sbd = str(sbd)
    bailam.made = str(md)
    
    bailam.save()
    
    return HttpResponseRedirect(reverse_lazy('danhsachbaithi'))

def laysbd(request, bailam_id):
    bailam = Bailam.objects.get(id=str(bailam_id))
    bl_url = bailam.bai.url
    sbd = get_sbd(bl_url)
    bailam.sbd = int(sbd)
    bailam.save()
    return HttpResponseRedirect(reverse_lazy('danhsachbaithi'))

class SuaBaithiView(UpdateView):
    model = Baithi
    form_class = BaithiForm
    template_name = 'quanlybaithi/suabaithi.html'
    # fields = '__all__'

class TaoBailamView(CreateView):
    model = Bailam
    template_name = 'quanlybaithi/taobailam.html'
    # fields = '__all__'
    form_class = BailamForm

class SuaBailamView(UpdateView):
    model = Bailam
    # fields = '__all__'
    form_class= BailamForm
    template_name = 'quanlybaithi/suabailam.html'

class XoaBailamView(DeleteView):
    model = Bailam
    template_name = 'quanlybaithi/xoabailam.html'
    success_url = reverse_lazy('danhsachbaithi')

class TaoBodapan(CreateView):
    model = Bodapan
    template_name = 'quanlybaithi/taodapan.html'
    fields = '__all__'