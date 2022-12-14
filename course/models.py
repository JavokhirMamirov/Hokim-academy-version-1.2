from django.db import models

from account.models import Teacher, Student

VIDEO_TYPES = (
    ("Youtube", "Youtube Link"),
    ("Video", "Video"),
    ("Vimeo", "Vimeo")
)

COURSE_TYPES = (
    (1, "Prezident maktabiga kiruvchilar uchun"),
    (2, "Abuturiyentlar uchun"),
    (3, "Xorijiy til o'rganuvchilar uchun"),
    (4, "O'qtuvchilar uchun"),
    (5, "Barcha uchun"),
)

LEVELS = (
    (1, "Boshlang'ich"),
    (2, "O'rta"),
    (3, "Murakkab")

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
    type = models.SmallIntegerField(choices=COURSE_TYPES, default=1)

    def __str__(self):
        try:
            return f"{self.name} ({self.get_type_display()})"
        except:
            return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    STEP = (
        (1, 'Yaratildi'),
        (2, "Darslar qo'shildi"),
        (3, "Testlar qo'shildi"),
        (4, 'Darslik yuklandi'),
        (5, "Ko'rib chiqilmoqda"),
        (6, 'Rad etildi'),
        (7, 'Taqdim etildi'),
    )
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    level = models.SmallIntegerField(default=1, choices=LEVELS)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='course/image/')
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    status = models.ForeignKey(CourseStatus, on_delete=models.SET_NULL, null=True, blank=True)
    course_type = models.SmallIntegerField(default=5, choices=COURSE_TYPES)
    is_recommended = models.BooleanField(default=False)
    best_three = models.BooleanField(default=False)
    step = models.SmallIntegerField(default=1, choices=STEP)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        try:
            return f"{self.title}-{self.teacher.full_name}"
        except:
            return self.title


class CourseAttachment(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course/attachment/', null=True, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    video_type = models.CharField(max_length=15, choices=VIDEO_TYPES, default="Youtube")
    video_link = models.CharField(max_length=255, null=True, blank=True)
    video = models.FileField(upload_to='course/video', null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)
    time = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=600)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    passed_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    query = models.TextField()
    optionA = models.TextField(max_length=900)
    optionB = models.TextField(max_length=900)
    optionC = models.TextField(max_length=900)
    optionD = models.TextField(max_length=900)
    correct_answer = models.TextField(max_length=900)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.query


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    time = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)


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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("CourseComment", on_delete=models.CASCADE, related_name='course_comment', null=True,
                               blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
