# serializers.py
from rest_framework import serializers
from student.models import student, Class, Author, Book
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from rest_framework_simplejwt.tokens import RefreshToken

class StudentSerializer(serializers.ModelSerializer):
    # class_info = serializers.SerializerMethodField() 
    year_birth = serializers.SerializerMethodField()
    
    class Meta:
        model = student
        fields = '__all__'

    def create(self, validated_data):
        avatar = validated_data.pop('avatar', None)

        student_n = student.objects.create(**validated_data)

        if avatar:
            student_n.avatar = avatar
            student_n.save()
        return student_n
    
    def validate(self, data):
        age = data.get('age')
        if age <= 0:
            raise serializers.ValidationError("Tuoi phai lon hon 0")
        return data
    
    # def get_class_info(self, student):
    #     return {
    #         "id": student.class_n.id,
    #         "name": student.class_n.name,
    #     }
    
    def get_year_birth(self, data):
        return timezone.now().year - data.age

class ClassSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=True, required=False)
    number_st = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['name', 'slug','student', 'number_st']
        read_only_fields = ['slug']

    def create(self, validated_data):
        students_data = validated_data.get('student', [])  # Sử dụng 'get' thay vì 'pop' để tránh KeyError
        validated_data['slug'] = slugify(validated_data['name'])
        new_class = Class.objects.create(**validated_data)

        for student_data in students_data:
            student_data['class_n'] = new_class
            student.objects.create(**student_data)

        return new_class
    
    def get_number_st(self, obj):
        return obj.student.count()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        
        # Convert the updated 'name' to 'slug' and update the 'slug' field
        updated_name = validated_data.get('name', instance.name)
        instance.slug = slugify(updated_name)

        instance.save()

        return instance
    
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model ='Book'
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author  # Thay YourClass bằng tên thực tế của class model
        fields = '__all__'

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

class AuthorSerializerCustom(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'firstname', 'lastname']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'username':
            {
                'required':False,
                'allow_null': True,
                'allow_blank': True 
            }
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Incorrect email/password")
        
        refresh = RefreshToken.for_user(user)
        refresh['email'] = email 
        return {
            'refresh': str(refresh),
            'access':str(refresh.access_token),
            'user_firstname': user.first_name,
            'user_lastname': user.last_name,
        }    
