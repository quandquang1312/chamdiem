from django import forms
from .models import Baithi, Bailam, Bodapan
from django.contrib.auth.models import User

class BaithiForm(forms.ModelForm):
    class Meta:
        model = Baithi
        fields = ('ten', 'created_by', 'socau')
        
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'ten-form'}),
            'created_by': forms.TextInput(attrs={'class': 'create-form', 'value': '', 'id': 'author', 'type': 'hidden'}),
            'socau': forms.TextInput(attrs={'class': 'ten-form'})
            # 'ketqua': forms.ImageField(),
        }

        labels = {
            'ten': ('Tên bài thi'),
            'socau': ('Số câu'),
            'ketqua': ('File ảnh đáp án')
        }

class BailamForm(forms.ModelForm):
    class Meta:
        model = Bailam
        fields = ('bai', 'baithi')

        widgets = {
            'hoten': forms.TextInput(attrs={'class': 'ten-form'}),
            'baithi': forms.TextInput(attrs={'id': 'baithi', 'value': '', 'type': 'hidden'})
        }

        labels = {
            'hoten': ('Họ và tên'),
            'bai': ('File ảnh bài làm'),
        }

class BodapanForm(forms.ModelForm):
    class Meta:
        model = Bodapan
        fields = ('baithi', 'dapan', 'bmade')

        widgets = {
            'baithi': forms.TextInput(attrs={'id': 'baithi', 'value': '', 'type': 'hidden'})
        }

        labels = {
            'dapan': ('File ảnh đáp án'),
            'bmade': ('Mã đề')
        }