from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Baithi(models.Model):
    id = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=155)
    thoigian = models.DateTimeField(default=timezone.now())
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ketqua = models.ImageField(upload_to='uploads/', blank=True, null=True)
    socau = models.IntegerField(default=0)

    def __str__(self):
        return self.ten

    def get_absolute_url(self):
        return reverse('danhsachbaithi')
    
class Bodapan(models.Model):
    id = models.AutoField(primary_key=True)
    baithi = models.ForeignKey(Baithi, on_delete=models.CASCADE)
    dapan = models.ImageField(upload_to='uploads/', blank=True, null=True)
    bmade = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.bmade

    def get_absolute_url(self):
        return reverse('danhsachbaithi')
    

class Bailam(models.Model):
    id = models.AutoField(primary_key=True)
    hoten = models.CharField(max_length=155)
    bai = models.ImageField(upload_to='uploads/', blank=True, null=True)
    diem = models.IntegerField(default=0)
    sbd = models.CharField(max_length=15, null=True)
    made = models.CharField(max_length=15, null=True)
    baithi = models.ForeignKey(Baithi, on_delete=models.CASCADE)

    def __str__(self):
        return self.hoten

    def get_absolute_url(self):
        return reverse('danhsachbaithi')