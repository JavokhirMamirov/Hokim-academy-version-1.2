from django.db.models import Q, Sum
from rest_framework import serializers

from api.teacher_api.serializers import CourseGetSerializer, TeacherSerializer
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


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'id',
            'title',
            'order',
            'videos',
        ]

    def get_videos(self, obj):
        try:
            videos = Lesson.objects.filter(section=obj).order_by('order')
            return LessonSerializer(videos, many=True)
        except:
            return []


class DetailCourseSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    test = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    teacher = TeacherSerializer()
    lessons_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'language',
            'description',
            'category',
            'level',
            'teacher',
            'image',
            'date_added',
            'course_type',
            'sections',
            'students',
            'tests',
            'lessons_count',
            'total_time'
        ]

    def get_total_time(self, obj):
        try:
            t_time = Lesson.objects.filter(
                section__course=obj
            ).aggregate(total=Sum('time')).get('total')

            if t_time is None:
                t_time = 0

            return t_time
        except:
            return 0

    def get_lessons_count(self, obj):
        try:
            lessons = Lesson.objects.filter(section__course=obj)
            return lessons.count()
        except:
            return 0

    def get_sections(self, obj):
        try:
            sections = Section.objects.filter(course=obj).order_by('order')
            return SectionSerializer(sections, many=True)
        except:
            return []

    def get_students(self, obj):
        try:
            query = WatchHistory.objects.filter(course=obj).count()
            return query
        except:
            return 0

    def get_tests(self, obj):
        return Quiz.objects.filter(course=obj).count()

    def get_language(self, obj):
        try:
            return obj.language.name
        except:
            return None

    def get_category(self, obj):
        try:
            return obj.category.name
        except:
            return None

    def get_level(self, obj):
        try:
            return obj.level.name
        except:
            return None

    def get_status(self, obj):
        try:
            return obj.status.name
        except:
            return None
