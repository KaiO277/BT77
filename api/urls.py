from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AuthorModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# router = DefaultRouter()
# router.register('st', views.StudentViewSet, basename='st')

router = DefaultRouter()
router.register(r'authors', AuthorModelViewSet, basename='author')

custom_get_by_id = views.StudentMVS.as_view({
    'get': 'custom_get_by_id'
})

get_list_api = views.StudentMVS.as_view({
    'get': 'get_list_student'
})

create_api = views.StudentMVS.as_view({
    'post': 'custom_create_st'
})

add_st_api = views.StudentMVS.as_view({
    'post': 'add_st_new'
})

test_update = views.StudentMVS.as_view({
    'patch':'test_update'
})

test_delete = views.StudentMVS.as_view({
    'delete':'test_delete'
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

get_all_class_by_user = views.StudentMVS.as_view({
    'get':'get_all_class_by_user'
})

get_test_query_param = views.StudentMVS.as_view({
    'get':'QueryParams'
})

get_test_path_params = views.StudentMVS.as_view({
    'get':'PathParams'
})

add_new_class = views.StudentMVS.as_view({
    'post':'add_new_class'
})

get_all_class2 = views.StudentMVS2.as_view({
    'get':'get_all_class'
})

get_all_class_limit = views.StudentMVS2.as_view({
    'get':'get_all_class_limit'
})

get_all_class_with_age = views.StudentMVS2.as_view({
    'get':'get_all_class_with_age'
})

get_all_class_info = views.StudentMVS2.as_view({
    'get':'get_all_class_info'
})

add_class = views.StudentMVS2.as_view({
    'post':'create_class'
})

update_class = views.StudentMVS2.as_view({
    'patch':'update_class'
})

login_user = views.UserLogin.as_view({
    'post':'login_user'
})

get_class_by_id = views.StudentMVS2.as_view({
    'get':'get_class_by_id'
})

delete_class_by_id = views.StudentMVS2.as_view({
    'delete': 'delete_class'
})

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
    path('get-all-class-by-user/', get_all_class_by_user, name='get-all-class-by-user'),
    path('get-query-param/', get_test_query_param, name="get-query-param"),
    path('get-path-param/<str:test>/<int:number>/', get_test_path_params, name='get-test-path-params'),   
    path('add-st-new/', add_st_api, name="add-st-new"),
    path('test-update/', test_update, name='test_update'),
    path('test-delete/', test_delete, name='test_delete'),
    path('add-new-class/', add_new_class, name='add-new-class'),
    path('get-all-class2/', get_all_class2, name='get_all_class2'),
    path('get-all-class-limit/', get_all_class_limit, name='get_all_class_limit'),
    path('get-all-class-with-age/', get_all_class_with_age, name='get-all-class-with-age'),
    path('get-all-class-info/', get_all_class_info, name='get_all_class_info'),
    path('create-add/', add_class, name='create-add'),
    path('update-class/<int:pk>/', update_class, name='update-class'),
    path('login-user/', login_user, name='login-user'),
    path('get-class-by-id/<int:pk>/', get_class_by_id, name='get-class-by-id'),
    path('delete-class-by-id/<int:pk>/', delete_class_by_id, name='delete-class-by-id'),
]
