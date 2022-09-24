from django.db import models

# Create your models here.
from account.models import City


class SchoolAriza(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25, null=True, blank=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeacherAriza(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    bio = models.TextField()
    about_course = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name