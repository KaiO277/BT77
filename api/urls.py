from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('st', views.StudentViewSet, basename='st')

custom_get_by_id = views.StudentMVS.as_view({
    'get': 'custom_get_by_id'
})

get_list_api = views.StudentMVS.as_view({
    'get': 'get_list_student'
})

create_api = views.StudentMVS.as_view({
    'post': 'custom_create_st'
})

put_api_id = views.StudentMVS.as_view({
    'put': 'custom_put_by_id'
})

patch_api_id = views.StudentMVS.as_view({
    'patch': 'custom_patch_by_id'
})

delete_api_id = views.StudentMVS.as_view({
    'delete': 'custom_delete_by_id'
})

all_student_attach_all_class = views.StudentMVS.as_view({
    'get':'get_all_student'
})

all_class_attach_all_student = views.StudentMVS.as_view({
    'get':'get_all_class'
})

urlpatterns = [
    # path('list-students', views.ListCreateStudentView.as_view()),
    # path('student', views.StudentViewset.as_view()),
    # path('student/<int:id>', views.StudentViewset.as_view()),
    path('students', views.student_list, name='student-list'),
    path('students/<int:id>', views.student_detail, name='student-detail'),
    path('', include(router.urls)),
    path('get-api/', get_list_api, name='get-api'),
    path('get-api/<int:pk>', custom_get_by_id, name='get-api'),
    path('create-api/', create_api, name='create-api'),
    path('put-api/<int:pk>', put_api_id, name='put-api'),
    path('patch-api/<int:pk>', patch_api_id, name='patch-api'),
    path('delete-api/<int:pk>',delete_api_id, name='delete-api'),
    path('get-all-student/', all_student_attach_all_class, name='get-all-student-attach-all-class'),
    path('get-all-class/', all_class_attach_all_student, name='get-all-class-attach-all-student'),
]
