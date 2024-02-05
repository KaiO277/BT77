from django.shortcuts import render
from student.models import student, Class
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from . import models
from .serializers import student_serializers
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify

class studentModelPagination(PageNumberPagination):
    page_size = 2  # Set the page size
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = student.objects.all()
    serializer_class = student_serializers.StudentSerializer
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
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data={
                'result': serializer.data
            }, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def test_distinct(self, request):
        result = student.objects.distinct('first_name')
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_first(self, request):
        result = student.objects.filter(age__gte=18).first()
        serializer = student_serializers.StudentSerializer(result, many=False)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_last(self, request):
        result = student.objects.filter(age__gte=18).last()
        serializer = student_serializers.StudentSerializer(result, many=False)
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
        result = student.objects.filter(first_name__icontains='nghia')
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_lcxkt(self, request):
        result = student.objects.filter(first_name='nghia0')
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    #gt: Greater than (Lớn hơn)
    @action(detail=False, methods=['get'])
    def test_gt(self, request):
        result = student.objects.filter(age__gt=20)
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(            
            data=serializer.data, status=status.HTTP_200_OK
        )

    #gte: Greater than or equal to (Lớn hơn hoặc bằng)
    @action(detail=False, methods=['get'])
    def test_gte(self, request):
        result = student.objects.filter(age__gte=20)
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    #lt: Less than(Nhỏ hơn)
    @action(detail=False, methods=['get'])
    def test_lt(self, request):
        result = student.objects.filter(age__lt=20)
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    # lte: Less than or equal to (Nhỏ hơn hoặc bằng)
    @action(detail=False, methods=['get'])
    def test_lte(self, request):
        result = student.objects.filter(age__lte=20)
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data= serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_null(self, request):
        result = student.objects.filter(avatar__isnull=True)
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def get_all_student(self, request):
        students = student.objects.all().select_related('name_class')
        serializer = student_serializers.StudentSerializer(students, many=True)
        print(serializer)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        ) 
    
    @action(detail=False, methods=['get'])
    def get_all_class(self, request):
        classs = Class.objects.all().prefetch_related('student')
        serializer = student_serializers.ClassSerializer(classs, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )


class StudentMVS(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = student.objects.all()
    serializer_class = student_serializers.StudentSerializer

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['get'])
    def get_all_student(self, request):
        students = student.objects.all().select_related('class_n')
        serializer = student_serializers.StudentSerializer(students, many=True)
        # print(serializer)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        ) 
    
    @action(detail=False, methods=['get'])
    def get_all_class(self, request):
        classs = Class.objects.all().prefetch_related('student')
        serializer = student_serializers.ClassSerializer(classs, many=True)
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
        serializer = student_serializers.StudentSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = student_serializers.StudentSerializer(data=request.data)
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
        serializer = student_serializers.StudentSerializer(item)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = student_serializers.StudentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PATCH':
        serializer = student_serializers.StudentSerializer(item, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    elif request.method == 'DELETE':
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)   