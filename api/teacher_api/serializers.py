from django.db.models import Sum
from rest_framework import serializers

from course.models import *


class CommentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'image']

class CommentTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'image']

class CourseCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = "__all__"


class CourseCommentGetSerializer(serializers.ModelSerializer):
    student = CommentStudentSerializer()
    teacher = CommentTeacherSerializer()
    class Meta:
        model = CourseComment
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'title', 'image', 'video']

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
            return LessonSerializer(videos, many=True).data
        except:
            return []

class SectionQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title']

class DetailCourseSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    tests = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    teacher = TeacherSerializer()
    lessons_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

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
            'status',
            'image',
            'date_added',
            'short_description',
            'course_type',
            'sections',
            'students',
            'tests',
            'lessons_count',
            'total_time',
            'is_saved'
        ]

    def get_is_saved(self, obj):
        try:
            user = self.context['request'].user
            query = WatchHistory.objects.filter(course=obj, student=user)
            if query.count() > 0:
                return True
            else:
                return False
        except:
            return False

    def get_total_time(self, obj):
        try:
            t_time = Lesson.objects.filter(
                section__course=obj
            ).aggregate(total=Sum('time')).get('total')

            if t_time is None:
                t_time = 0

            s = t_time // 60
            m = t_time % 60
            if s > 0:
                time = f"{s} s {m} min"
            else:
                time = f"{m} min"

            return time
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
            query = Section.objects.filter(course=obj).order_by('order')
            return SectionSerializer(query, many=True).data
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

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'full_name',
            'title',
            'username',
            'email',
            'biography',
            'video',
            'image',
            'website',
            'instagram',
            'facebook',
            'telegram',
            'date_added',
        ]


class MyStudentSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
            'id',
            'full_name',
            'phone',
            'image',
            'status',
            'school',
            'course_count',
        ]

    def get_school(self, obj):
        try:
            return obj.school.name
        except:
            return ""

    def get_status(self, obj):
        return obj.get_status_display()

    def get_course_count(self, obj):
        try:
            teacher = self.context['request'].user
            courses = WatchHistory.objects.filter(course__teacher=teacher, student=obj)
            return courses.count()
        except:
            return 1


class MyCourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    step = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "short_description",
            "language",
            "category",
            "level",
            "image",
            "date_added",
            "status",
            "lessons_count",
            "course_type",
            "total_time",
            "step"
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

    def get_course_type(self, obj):
        return obj.get_course_type_display()

    def get_step(self, obj):
        return obj.get_step_display()

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


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseGetSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    lessons_count = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "short_description",
            "language",
            "category",
            "level",
            "teacher",
            "image",
            "date_added",
            "status",
            "lessons_count",
            "course_type",
            "total_time",
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
    query_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'course',
            'level',
            'query_count',
            'section',
            'time',
            'order',
            'questions',
            'passed_percent',
            'is_active',
        ]

    def get_query_count(self, obj):
        try:
            query = Question.objects.filter(quiz=obj)
            return query.count()
        except:
            return 0

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
