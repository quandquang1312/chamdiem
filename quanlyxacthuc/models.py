from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hoten = models.TextField()
    sdt = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("thongtin")
    