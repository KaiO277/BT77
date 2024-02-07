from rest_framework import serializers
from student.models import student, Class
from django.utils import timezone



class StudentSerializer(serializers.ModelSerializer):
    # class_info = serializers.SerializerMethodField()
    # year_birth = serializers.SerializerMethodField()

    class Meta:
        model = student 
        fields = '__all__'
        # fields = ['first_name','last_name','age','year_birth', 'class_n', 'created_at']

    def create(self, validated_data):
        avatar = validated_data.pop('avatar', None)

        student_n = student.objects.create(**validated_data)

        if avatar:
            student_n.avatar = avatar
            student_n.save()

        return student_n    
    
    def get_class_info(self, obj):
        class_info = {
            # "id" : obj.class_n.id,
            "name" : obj.class_n.name, 
        }
        return class_info
        
    # def validate(self, data):
    #     age = data.get('age')
    #     if age < 1:
    #         raise serializers.ValidationError("Tuổi phải lớn hơn 0")
    #     return data
    
    # def get_year_birth(self, data):
    #     return timezone.now().year-data.age
    
class ClassSerializer(serializers.ModelSerializer):
    # student = StudentSerializer( many=False, read_only=True)
    student = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = '__all__'    

