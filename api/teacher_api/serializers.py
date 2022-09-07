from rest_framework import serializers

from course.models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'title', 'image']


class CourseGetSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    lessons_count = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "short_description",
            "language",
            "category",
            "sub_category",
            "level",
            "teacher",
            "video",
            "video_type",
            "image",
            "date_added",
            "status",
            "lessons_count",
            "course_type",
            "total_time",
        ]

    def get_lessons_count(self, obj):
        try:
            lessons = Lesson.objects.filter(section__course=obj)
            return lessons.count()
        except:
            return 0

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

    def get_sub_category(self, obj):
        try:
            return obj.sub_category.name
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


class CoursePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAttachment
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuizGETSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'course',
            'level',
            'query_count',
            'time',
            'order',
            'questions',
            'passed_percent',
            'is_active',
        ]

    def get_questions(self, obj):
        try:
            queries = Question.objects.filter(quiz=obj)
            ser = QuestionSerializer(queries, many=True)
            return ser.data
        except:
            return []


class QuizPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseLessonsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'course', 'title', 'order', 'lessons']

    def get_lessons(self, obj):
        try:
            less = Lesson.objects.filter(section=obj)
            return LessonSerializer(less, many=True).data
        except:
            return []
