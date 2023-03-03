from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.core.validators import FileExtensionValidator

class User(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    ADMIN = 1
    STUDENT = 2
    LECTURER = 3
    user_type = (
        (ADMIN, "Admin"),
        (LECTURER, "Lecturer"),
        (STUDENT, "Student"),
    )
    user_type = models.PositiveSmallIntegerField(choices=user_type, verbose_name="User Types", default=ADMIN)
    username = models.CharField(_('Username'),max_length=50, blank=True,null=True)
    email =  models.EmailField(_('Email address'),unique=True, blank=True,null=True)
    mobile_number = PhoneNumberField(null=True, blank=True, unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True,null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    profiles = models.FileField(upload_to='profiles', null=True, verbose_name='user profile',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp'])])
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, blank=True,null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return self.username


class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Course(models.Model):
    BACHELOR_DEGREE = "Bachelor"
    MASTER_DEGREE = "Master"

    LEVEL = (
        (BACHELOR_DEGREE, "Bachelor Degree"),
        (MASTER_DEGREE, "Master Degree"),
    )
    course_id = models.CharField(_("course_id"), max_length=200, unique=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    description  = models.TextField()
    department = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.course_id:
            max_id = Course.objects.aggregate(id_max=Max('id'))['id_max']
            self.course_id = "{}{:03d}".format('C', (max_id + 1) if max_id is not None else 1)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='allocated_lecturer')
    courses = models.ManyToManyField(Course,related_name='allocated_course')

    def __str__(self):
        return self.lecturer.get_full_name

class TimePeriod(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return str(self.start_year)  + " --- " + str(self.end_year)


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    student_id = models.CharField(_("student_id"), max_length=200, unique=True, blank=True)
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    period = models.ForeignKey(TimePeriod,on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            max_id = Student.objects.aggregate(id_max=Max('id'))['id_max']
            self.student_id = "{}{:03d}".format('S', (max_id + 1) if max_id is not None else 1)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')

    def __str__(self):
        return "{0} ({1})".format(self.course.title, self.course.course_id)