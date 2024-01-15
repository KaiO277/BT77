from django.db import models

# Create your models here.

class student(models.Model):
    first_name = models.TextField(max_length=250, null=True, blank=True)
    last_name = models.TextField(max_length=250, null=True, blank=True)
    age = models.IntegerField(null=True, blank = True)

    def __str__(self):
        return self.first_name
