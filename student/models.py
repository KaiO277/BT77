from django.db import models
import os
from datetime import datetime
from rest_framework import serializers
from django.conf import settings

# Create your models here.

def avatar_file_name(instance, filename):
    ext = filename.split('.')[-1]
    name = filename.split('.')[0]
    
    filename = f"{name}_{datetime.now().strftime('%d_%m_%Y')}.{ext}"

    return os.path.join('avatar/', filename)

class Class(models.Model):
    name = models.TextField(max_length=250)

    def __str__(self):
        return self.name


class student(models.Model):
    first_name = models.TextField(max_length=250)
    last_name = models.TextField(max_length=250)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class_n = models.ForeignKey(Class, on_delete=models.CASCADE, related_name = 'student', blank = True, null = True)
    avata = models.ImageField(upload_to=avatar_file_name, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'student', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name
