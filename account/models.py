from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser

from random import randint
import secrets
import string

from home.packages.certificate_generate import certificate_generate


def generate_promokod():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    return password


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    lat = models.CharField(max_length=255, null=True, blank=True)
    lng = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Account(AbstractUser):
    STATUS_CHOICES = (
        (1, "Admin"),
        (2, "Ta'lim boshqarmasi"),
        (3, "Maktab xodimi"),
    )
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICES)


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    STUDENT_TYPES = (
        (1, "Prezident Maktabiga"),
        (2, "Abuturent"),
        (3, "Xorijiy til o'rganuvchi"),
        (4, "O'qtuvchi"),
    )
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    start_study_year = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(default=1, choices=STUDENT_TYPES)
    promo_code = models.CharField(max_length=10, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    certificate = models.ImageField(upload_to='certificate/', null=True, blank=True)
    password = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    is_used_promocode = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.promo_code = generate_promokod()
            self.password = make_password(self.promo_code)

            while True:
                username = f'student-{randint(1, 9999999)}'
                query = Student.objects.filter(username=username)
                if query.count() == 0:
                    self.username = username
                    break
            self.certificate = certificate_generate(self)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
