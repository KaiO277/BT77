from django.urls import path
from . import views

urlpatterns = [
    path('list-students/', views.list_students, name='list-students'),
]
