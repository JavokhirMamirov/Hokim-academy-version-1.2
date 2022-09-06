from django.db import models

from account.models import Teacher, Student

VIDEO_TYPES = (
    ("Youtube", "Youtube Link"),
    ("Video", "Video"),
    ("Vimeo", "Vimeo")
)

COURSE_TYPES = (
    (1, "Prezident Maktabiga kiruvchilar uchun"),
    (2, "Abuturentlar uchun"),
    (3, "Xorijiy til o'rganuvchilar uchun"),
    (4, "O'qtuvchilar uchun"),
    (5, "Barcha uchun"),
)


class Language(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class CourseStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    STEP = (
        (1, 'Lesson adding'),
        (2, 'Quiz adding'),
        (3, 'Finished'),
        (4, 'Checking'),
        (5, 'Canceled'),
        (6, 'Published'),
    )
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPES)
    image = models.ImageField(upload_to='course/image/')
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    status = models.ForeignKey(CourseStatus, on_delete=models.SET_NULL, null=True, blank=True)
    course_type = models.SmallIntegerField(default=5, choices=COURSE_TYPES)
    total_time = models.IntegerField(default=0)
    is_recommended = models.BooleanField(default=False)
    best_three = models.BooleanField(default=False)
    step = models.SmallIntegerField(default=1, choices=STEP)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class LessonAttachment(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course/attachment/')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    video_type = models.CharField(max_length=15, choices=VIDEO_TYPES, default="Youtube")
    video = models.CharField(max_length=255, null=True)
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now_add=True)
    summary = models.TextField(null=True)
    attachment = models.ManyToManyField(LessonAttachment, blank=True)
    time = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=600)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    query_count = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    passed_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    query = models.TextField()
    optionA = models.CharField(max_length=255)
    optionB = models.CharField(max_length=255)
    optionC = models.CharField(max_length=255)
    optionD = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.query


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_submited = models.BooleanField(default=False)


class QuizAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.CharField(max_length=255)
    result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)


class WatchHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lesson = models.ManyToManyField(Lesson)
    course_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    watching_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='watching_lesson')
    quiz_result = models.ManyToManyField(QuizResult)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Rating(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    review = models.TextField()


class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey("CourseComment", on_delete=models.CASCADE, related_name='course_comment', null=True,
                               blank=True)
    comment = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
