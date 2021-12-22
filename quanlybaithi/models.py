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

    def __str__(self):
        return self.ten

    def get_absolute_url(self):
        return reverse('danhsachbaithi')
    
