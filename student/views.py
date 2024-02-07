from django.shortcuts import render
from .models import student, Class
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from . import models
from .serializers import student_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Count


# from django_filters import rest_framework as django_filters
# from rest_framework import permissions

# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = student.objects.all()
    serializer_class = student_serializers.StudentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    # search_fields = ['first_name', 'age']
    # ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering not in ['created_at', '-created_at']:
            ordering = 'created_at'

        # Search by 'first_name' and 'age' (taken care of by SearchFilter)
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
                pass  # Handle error if 'min_age' or 'max_age' is not a valid integer

        queryset = queryset.filter(conditions).order_by(ordering)
        return queryset

    @action(detail=False, methods=['get'])
    def test_count(self, request):
        count = student.objects.filter(age=14).count()
        return Response(
            data={
                'count': count
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_exclude(self, request):
        result = student.objects.exclude(age=14)
        serializer = student_serializers.StudentSerializer(result,many=True)
        return Response(
            data={
                'result': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_distinct(self, request):
        result = student.objects.filter(age__gte=15).distinct()
        serializer = student_serializers.StudentSerializer(result, many=True)
        return Response(
            data= serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_first(self, request):
        result = student.objects.filter(age__gte=14).first()
        serializer = student_serializers.StudentSerializer(result, many=False)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def test_last(self, request):
        result = student.objects.filter(age__gte=14).last()
        serializer = student_serializers.StudentSerializer(result, many=False)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def test_slug(self, request):
        result = student.objects.filter()


    @action(detail=True, methods=['get'])
    def get(self, request, pk=None):
        # Lấy thông tin chi tiết của một sinh viên
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_student(self, request):
        # Lấy danh sách tất cả sinh viên
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def custom_patch(self, request, pk=None):
        # Cập nhật thông tin của một sinh viên (tương đương với hàm patch trước đây)
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def custom_put(self, request, pk=None):
        # Cập nhật thông tin của một sinh viên (tương đương với hàm patch trước đây)
        student_instance = self.get_object()
        serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def custom_delete(self, request, pk=None):
        # Xóa một sinh viên (tương đương với hàm delete trước đây)
        student_instance = self.get_object()
        student_instance.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def custom_create(self, request):
        # Thêm mới một sinh viên (tương đương với hàm post trước đây)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = student.objects.all()
    serializer_class = student_serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = student.objects.all()
    serializer_class = student_serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentMVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = student_serializers.ClassSerializer


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def student_list(request):
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

@api_view(['GET','PATCH', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def student_detail(request, id):
    try:
        item = student.objects.get(id=id)
    except student.DoesNotExist:
        return Response({"status": "error", "data": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = student_serializers.StudentSerializer(item)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = student_serializers.StudentSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        serializer = student_serializers.StudentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)    
    
# @permission_classes([permissions.IsAuthenticated])
class StudentViewSet1(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = student.objects.all()
    serializer_class = student_serializers

    # Custom action để thêm mới sinh viên
    @action(detail=False, methods=['post'])
    def create_student(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    # Custom action để lấy danh sách sinh viên
    @action(detail=False, methods=['get'])
    def list_students(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Custom action để cập nhật sinh viên
    @action(detail=True, methods=['put'])
    def update_student(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Custom action để xóa sinh viên
    @action(detail=True, methods=['delete'])
    def delete_student(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_student(self, request, pk=None):
        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def getAllStudent(self, request):
        students = student.objects.all().select_related('class_n')
        serializer = student_serializers.StudentSerializer(students, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def getAllClass(self, request):
        classs = Class.objects.all().prefetch_related('student')
        serializer = student_serializers.ClassSerializer(classs, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def getAllClassbyUser(self, request, *args, **kwargs):
        # user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
        user = request.user
        print(user.id)
        queryset = Class.objects.annotate(
        user_student_count=Count(
            Case(
                When(student__user=user.id, then=Value(1)),
                output_field=IntegerField(),
            )
        )
        ).filter(user_student_count__gt=0)
        classs = Class.objects.filter(student__user=user).distinct()
        print(queryset)
        serializer = student_serializers.ClassSerializer(classs, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
