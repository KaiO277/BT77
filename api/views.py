from django.shortcuts import render
from student.models import student, Class, Author, Book
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from . import models
# from . import views
# from . import student_serializers
from .student_serializers import UserLoginSerializer,StudentSerializer, AuthorSerializer, AuthorSerializerCustom, ClassSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify
from .statuscode import StatusCode
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class AuthorModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset= Author.objects.all()
    
    def get_serializer_class(self):
        return self.get_author_serializer()

    def get_author_serializer(self):
        if self.action == 'list':
            return AuthorSerializer
        else:
            return AuthorSerializerCustom

class studentModelPagination(PageNumberPagination):
    page_size = 2  # Set the page size
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    # pagination_class = studentModelPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering not in ['created_at', '-created_at']:
            ordering = 'created_at'

        first_name = self.request.query_params.get('first_name', None)
        min_age = self.request.query_params.get('min_age', None)
        max_age = self.request.query_params.get('max_age', None)

        conditions = Q()

        if first_name:
            conditions &= Q(first_name__icontains=first_name.lower())

        if min_age and max_age:
            try:
                min_age = int(min_age)
                max_age = int(max_age)
                conditions &= Q(age__range=[min_age, max_age])
            except ValueError:
                pass  

        if ordering == '-created_at':
            queryset = queryset.filter(conditions).order_by('-created_at')
        else:
            queryset = queryset.filter(conditions).order_by('created_at')

        return queryset

    @action(detail=False, methods=['get'])
    def test_count(self, request):
        count = student.objects.filter(age=20).count()
        return Response(
            data={
                'count': count
            }, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_exclude(self, request):
        result = student.objects.filter(first_name='kaio').exclude(age__lte=20)
        serializer = StudentSerializer(result, many=True)
        return Response(
            data={
                'result': serializer.data
            }, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def test_distinct(self, request):
        result = student.objects.distinct('first_name')
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_first(self, request):
        result = student.objects.filter(age__gte=18).first()
        serializer = StudentSerializer(result, many=False)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_last(self, request):
        result = student.objects.filter(age__gte=18).last()
        serializer = StudentSerializer(result, many=False)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def test_slug(self, request):
        result = student.objects.filter(age__gte=18).first()
        
        result_slug= slugify(result.first_name)
        return Response(
            data={
                'slug': result_slug,
                'first_name': result.first_name,
            }, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def custom_get_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def custom_list_student(self, request):
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def custom_patch_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def custom_put_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)        

    @action(detail=True, methods=['delete'])
    def custom_delete_id(self, request, pk=None):
        student_instance = self.get_object()
        student_instance.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def custom_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def test_lckt(self, request):
        result = student.objects.filter(first_name__icontains='w')
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_lcxkt(self, request):
        result = student.objects.filter(first_name='nghia0')
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    #gt: Greater than (Lớn hơn)
    @action(detail=False, methods=['get'])
    def test_gt(self, request):
        result = student.objects.filter(age__gt=20)
        serializer = StudentSerializer(result, many=True)
        return Response(            
            data=serializer.data, status=status.HTTP_200_OK
        )

    #gte: Greater than or equal to (Lớn hơn hoặc bằng)
    @action(detail=False, methods=['get'])
    def test_gte(self, request):
        result = student.objects.filter(age__gte=20)
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    #lt: Less than(Nhỏ hơn)
    @action(detail=False, methods=['get'])
    def test_lt(self, request):
        result = student.objects.filter(age__lt=20)
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    # lte: Less than or equal to (Nhỏ hơn hoặc bằng)
    @action(detail=False, methods=['get'])
    def test_lte(self, request):
        result = student.objects.filter(age__lte=20)
        serializer = StudentSerializer(result, many=True)
        return Response(
            data= serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_null(self, request):
        result = student.objects.filter(avatar__isnull=True)
        serializer = StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def get_all_student(self, request):
        students = student.objects.all().select_related('name_class')
        serializer = StudentSerializer(students, many=True)
        print(serializer)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        ) 
    
    @action(detail=False, methods=['get'])
    def get_all_class(self, request):
        classs = Class.objects.all().prefetch_related('student')
        serializer = ClassSerializer(classs, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    

def validate_age(age):
    return student.objects.filter(age=age).exists()

def validate_email(email):
    return student.objects.filter(email=email).exists() 

def check_slug(name):
    slug = slugify(name)
    return Class.objects.filter(slug=slug).exists()

class UserLogin(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'])
    def login_user(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                data=serializer.validated_data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class StudentMVS2(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Class.objects.all()

    @action(detail=True, methods=['get'])
    def get_class_by_id(self, request, pk=None):
        try:
            classes = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClassSerializer(classes)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_class(self, request, pk=None):
        try:
            classes = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClassSerializer(classes)
        return Response(status=status.HTTP_204_NO_CONTENT)        

    @action(detail=False, methods=['patch'])
    def update_class(self, request, pk=None):
        try:
            classes = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response({"message":"Error"}, status=status.HTTP_400_BAD_REQUEST)
        if 'name' in request.data:
            if check_slug(request.data['name']):
                return Response(
                    {"Message":"Slug already exists"}, status=StatusCode.SLUG_EXIS
                )    
            else:
                serializer = ClassSerializer(classes, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else: 
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_class(self, request):
        name = request.data.get('name')
        if check_slug(name):
            return Response({"message":"tên lớp đã trùng"}, status=StatusCode.SLUG_EXIS)
        else:
            serializer = ClassSerializer(data=request.data)  # Pass 'data' argument
            print(request.data)
            if serializer.is_valid():  # Check if the serializer is valid
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Dữ liệu không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def get_all_class(self, request):
        number_limit = int(self.request.query_params.get('so_luong',0))
        if number_limit >0:
            classes = Class.objects.all()[:number_limit]
        else:
            classes = Class.objects.all()        
        serializer = ClassSerializer(classes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods="get")
    def get_all_class_limit(self, request):
        number_limit = int(self.request.query_params.get('so_luong', 0))
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)

        if number_limit > 0:
            # Sử dụng filter và lambda để lọc dữ liệu
            serializer_data = list(filter(lambda obj: obj.get('number_st', 0) <= number_limit, serializer.data))
            return Response(data=serializer_data, status=status.HTTP_200_OK)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def get_all_class_with_age(self, request):
        min = self.request.query_params.get('age_min')
        max = self.request.query_params.get('age_max')

        min = int(min) if min is not None else 0
        max = int(max) if max is not None else int('inf')

        classes = Class.objects.filter(student__age__gt=min, student__age__lt=max)
        serializer = ClassSerializer(classes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return ClassSerializer
    #     else:
    #         return ClassSerializerCustom

    # @action(detail=False, methods=["get"])
    # def get_all_class_info(self, request):
    #     class_instance = self.get_object()
    #     serializer = self.get_serializer(class_instance)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class StudentMVS(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(detail=True, methods=['get'])
    def get_all_class_by_user(self, request, *args, **kwargs):
        user_id = request.user
        print(user_id)

        class_data = Class.objects.filter(student__user=user_id).distinct()
        serializer = ClassSerializer(class_data, many=True)

        return Response(
            data={
               "user_class_info": serializer.data,
            },
            status=status.HTTP_200_OK
        )   

    @action(detail=False, methods=['post'])
    def add_new_class(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def add_st_new(self, request):
        email = request.data.get('email')
        age = request.data.get('age')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if validate_age(age) & validate_email(email):
                return Response(
                    data={"message":"AGE_AND_EMAIL_EXIS"},
                    status= StatusCode.AGE_AND_EMAIL_EXIS
                )
            elif validate_age(age):
                return Response(
                    data={"message":"age already exis"},
                    status=StatusCode.AGE_ALREADY_EXIS
                )
            elif validate_email(email):
                return Response(
                    data={"message":"email already exis"},
                    status = StatusCode.EMAIL_ALREADY_EXIS
                )

    # @action(detail=False, methods=['get'])
    # def get_all_class(self, request):
    #     user = request.user
    #     number_limit = int(self.request.query_params.get('so_luong',0))
    #     if number_limit >0:
    #         classes = Class.objects.all()[:number_limit]
    #     else:
    #         classes = Class.objects.all()        
    #     serializer = ClassSerializer(classes, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_all_class(self, request):
        classs = Class.objects.all()
        serializer = ClassSerializer(classs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def QueryParams(self, request):
        param_test = self.request.query_params.get('test')
        param_number = self.request.query_params.get('number')
        if param_test is not None and param_number is not None:
            return Response(
                {
                    'param_test': param_test,
                    'param_number': param_number
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'param_test': "NULL",
                    'param_number': 'NULL'
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def PathParams(self, request, *args, **kwargs):
        param_test = self.kwargs.get('test')
        param_number = self.kwargs.get('number')

        if param_test is not None and param_number is not None:
            return Response(
                {
                    'param_test': param_test,
                    'param_number': param_number
                }, 
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'param_test': "NULL",
                'param_number': 'NULL'
            }, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['get'])
    def test(self, request, pk=None):
        try:
            class_o = self.get_object()
            if class_o:
                return Response({'status':'successful'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Error', status=status.HTTP_400_BAD_REQUEST)    
    
    # @action(detail=True, methods=['get'])
    # def get_all_class_by_user(seld, request):
    #     user = request.user
    #     print(user.id)
    #     classs = Class.objects.filter(student__user=user).distinct()
    #     # print(student__user)
    #     serializer = ClassSerializer(classs, many=True)
    #     return Response(
    #         data=serializer.data, status=status.HTTP_200_OK
    #     )
        
    # @action(detail=True, methods=['get'])
    # def get_all_class_by_user(self, request, *args, **kwargs):
    #     user = request.user

        # Lọc các sinh viên thuộc lớp mà người dùng hiện tại đã tham gia
        # student_classes = Class.objects.filter(student__user=user)
        # .distinct()
        # se = ClassSerializer(student_classes, many=True)
        # print(se.data)

        # Tạo một danh sách chứa thông tin lớp và sinh viên của người dùng hiện tại
        # user_class_info = []

        # for student_class in student_classes:
        #     class_info = ClassSerializer(student_class).data
        #     students = student_class.student.filter(user=user)
        #     student_info = StudentSerializer(students, many=True).data
        #     class_info['student'] = student_info
        #     user_class_info.append(class_info)
        # classs = Class.objects.prefetch_related(
        #     Prefetch('student', queryset=student.objects.filter(user=user.id), to_attr='filtered_students')
        # ).all()
        # class_data = ClassSerializer(classs, many=True)

        # return Response(
        #     data={
        #        "user_class_info": class_data,
        #     #    "se":se.data
        #     } ,
        #     status=status.HTTP_200_OK
        # )

    @action(detail=True, methods=['get'])
    def custom_get_by_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_list_student(self, request):
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def custom_patch_by_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def custom_put_by_id(self, request, pk=None):
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)        

    @action(detail=True, methods=['delete'])
    def custom_delete_by_id(self, request, pk=None):
        student_instance = self.get_object()
        student_instance.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def custom_create_st(self, request):
        # age = request.data.get('age')
        # email = request.data.get('email')
        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     if validate_age(age) & validate_email(email):
        #         return Response(
        #             data={
        #                 "message":"email and age already exis"
        #             }, status=StatusCode.AGE_AND_EMAIL_EXIS
        #         )
        #     elif validate_email(email):
        #         return Response(
        #             data={"message":"email already exis"}, 
        #             status=StatusCode.EMAIL_ALREADY_EXIS
        #         )
        #     elif validate_age(age):
        #         return Response(
        #             data={"message":"age already exis"},
        #             status=StatusCode.AGE_ALREADY_EXIS
        #         )
        #     else:
        #         serializer.save()
        #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   
        
    @action(detail=False, methods=['post'])
    def custom_create_st_new(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=['delete'])
    def test_delete(self, request):
        try:
            student.objects.filter(first_name="nghia00").delete()
            return Response(
                data={"message":"Done"},
                status=status.HTTP_200_OK
            )
        except student.DoesNotExist:
            return Response(
                data={"message":"error"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=True, methods=['patch'])
    def test_update(self, request):
        try:
            student.objects.filter(first_name="nghia00").update(age=22)
            return Response(
                data={"message":"Done"},
                status=status.HTTP_200_OK
            )
        except student.DoesNotExist:
            return Response(data={"message":"student..."}, status=status.HTTP_404_NOT_FOUND) 
    
    @action(detail=True, methods=['get'])
    def get_all_student(self, request):
        students = student.objects.all().select_related('class_n')
        serializer = StudentSerializer(students, many=True)
        # print(serializer)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        ) 
    
    @action(detail=True  , methods=['get'])
    def get_all_class(self, request):
        user = user.request
        classs = Class.objects.all().prefetch_related(student__user=user)
        serializer = ClassSerializer(classs, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        ) 
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def student_list(request):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    if request.method == 'GET':
        items = student.objects.all()
        serializer = StudentSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def student_detail(request, id):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    try:
        item = student.objects.get(id=id)
    except student.DoesNotExist:
        return Response({"status": "error", "data": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(item)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PATCH':
        serializer = StudentSerializer(item, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    elif request.method == 'DELETE':
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)   