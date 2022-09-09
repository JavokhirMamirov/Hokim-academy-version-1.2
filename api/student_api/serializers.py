from django.db.models import Q
from rest_framework import serializers

from api.teacher_api.serializers import CourseGetSerializer
from course.models import *


class StudentSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'full_name',
            'birth_date',
            'start_study_year',
            'phone',
            'address',
            'image',
            'status',
            'username',
            'telegram',
            'facebook',
            'instagram',
            'website',
            'school',
        ]

    def get_school(self, obj):
        try:
            return obj.shool.name
        except:
            return None

    def get_status(self, obj):
        return obj.get_status_display()


class CourseSerializerForCard(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseHomeWithCategorySerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'course']

    def get_course(self, obj):
        try:
            user = self.context['request'].user
            courses = Course.objects.filter(Q(category=obj), Q(course_type=user.status) | Q(category__type=5),
                                            Q(step=7))[0:12]

            ser = CourseGetSerializer(courses, many=True)
            return ser.data
        except:
            return []

class SearchCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'image']
