from django.urls import path, include
from . import views
from .views import student_list, student_detail
from student.views import StudentMVS
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('st', views.StudentViewSet, basename='st')

get_all_student = views.StudentViewSet1.as_view({
    'get':'getAllStudent'
})

get_all_class = views.StudentViewSet1.as_view({
    'get':'getAllClass'
})

get_all_class_by_user = views.StudentViewSet1.as_view({
    'get':'getAllClassbyUser'
})

urlpatterns = [
    path('student/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('student/<int:id>', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/', student_list, name='student-list'),
    path('students/<int:id>/', student_detail, name='student-detail'),
    path('', include(router.urls)),
    path('get-all-student/',get_all_student, name='get-all-student'),
    path('get-all-class/', get_all_class, name='get-all-class'),
    path('get-all-class-by-user/', get_all_class_by_user, name='get-all-class-by-user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()