from rest_framework import serializers

from api.student_api.serializers import QuizResultSerializer
from course.models import Course, WatchHistory, Quiz, Question, QuizResult


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title']


class QuizGetResultSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = QuizResult
        fields = ['id', "student", 'quiz']

    def get_student(self, obj):
        return obj.student.full_name

    def get_quiz(self, obj):
        return obj.quiz.title


class QuizDetailSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "course",
            "time",
            "order",
            "passed_percent",
            "result",
            'question_count'
        ]

    def get_question_count(self, obj):
        questions = Question.objects.filter(quiz=obj)
        return questions.count()

    def get_result(self, obj):
        try:
            student = self.context['student']
            query = QuizResult.objects.filter(student=student, quiz=obj).last()
            ser = QuizResultSerializer(query)
            return ser.data
        except:
            return None


class CourseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title"]


class MyCourseSerializer(serializers.ModelSerializer):
    course = CourseGetSerializer()

    class Meta:
        model = WatchHistory
        fields = ['id', 'course']
