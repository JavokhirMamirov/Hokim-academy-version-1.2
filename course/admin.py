from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    search_fields = ['name']
    list_filter = ['type']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "short_description",
        "language",
        "level",
        "teacher",
        "status",
        "course_type",
        "is_recommended",
        "best_three",
        "is_active",
    ]
    list_filter = ['language', 'category', 'teacher', 'step', 'best_three']
    search_fields = ['title']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order']
    search_fields = ['title']
    list_filter = ['course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'section', 'video_type', 'summary',  'date_added']
    search_fields = ['title']
    list_filter = ['section']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'level', 'order', 'passed_percent', 'is_active', 'time']
    list_filter = ['course', 'section', 'is_active']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'quiz',
                    'query',
                    'optionA',
                    'optionB',
                    'optionC',
                    'optionD',
                    'correct_answer',
                    'order',
                    ]
    list_filter = ['quiz']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['id',
                    "quiz",
                    "student",
                    "mark",
                    "date_added",
                    "date_updated",
                    "is_passed",
                    'time'
                    ]
    list_filter = ['quiz']


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'student_answer', 'result']


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'student',
                    'course',
                    'course_progress',
                    'watching_lesson',
                    'date_added',
                    'date_updated',
                    ]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating', 'student', 'course', 'date_added']


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'course',
                    'student',
                    'parent',
                    'comment',
                    'date_added',
                    ]
    list_filter = ['course']