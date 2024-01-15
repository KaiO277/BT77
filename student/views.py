from django.shortcuts import render
from .models import student
from django.http import JsonResponse

# Create your views here.

def list_students(request):
    students = student.objects.all()
    student_list = [{'first_name': student.first_name, 'last_name': student.last_name, 'age': student.age} for student in students]
    return JsonResponse({'students': student_list})