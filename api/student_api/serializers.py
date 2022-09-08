from rest_framework import serializers

from api.teacher_api.serializers import CourseGetSerializer
from course.models import *


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
            courses = Course.objects.filter(category=obj, step=7)[0:12]

            ser = CourseGetSerializer(courses, many=True)
            return ser.data
        except:
            return []


