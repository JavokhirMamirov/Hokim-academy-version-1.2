from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']




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


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order']


@admin.register(LessonAttachment)
class LessonAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'section', 'video_type', 'summary',  'date_added']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'level', 'order', 'query_count', 'passed_percent', 'is_active', 'time']


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


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['id',
                    "quiz",
                    "student",
                    "mark",
                    "date_added",
                    "date_updated",
                    "is_submited",
                    ]


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
