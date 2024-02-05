from django.db import models
import os
from datetime import datetime

# Create your models here.

def avatar_file_name(instance, filename):
    ext = filename.split('.')[-1]
    name = filename.split('.')[0]

    filename = f"{name  }_{datetime.now().strftime('%d_%m_%Y')}.{ext}"

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
    avatar = models.ImageField(upload_to=avatar_file_name, null=True, blank=True)
    class_n = models.ForeignKey(Class,on_delete=models.CASCADE,related_name = 'student', blank = True, null=True)

    def __str__(self):
        return self.first_name
    
class Author(models.Model):
    firstname = models.CharField(blank=True, null=True)
    lastname = models.CharField(blank=True, null=True)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Book(models.Model):
    title = models.CharField(blank=True, null=True, max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book', blank=True, null=True)

    def __str__(self):
        return self.title


