from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Max


class User(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    username = models.CharField(_('Username'),max_length=50, blank=True,null=True)
    email =  models.EmailField(_('Email address'),unique=True, blank=True,null=True)
    mobile_number = PhoneNumberField(null=True, blank=True, unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True,null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True,null=True)
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

    def __str__(self):
        return self.email


class AdmissionYear(models.Model):
    admission_start_year = models.DateTimeField()
    admission_end_year = models.DateTimeField()


class HodDetails(models.Model):
    """Database model for ADMIN OR HOD in the system"""

    hod_id = models.CharField(_("hod_id"), max_length=200, unique=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = 'HOD'

    def save(self, *args, **kwargs):
        if not self.hod_id:
            max_id = HodDetails.objects.aggregate(id_max=Max('id'))['id_max']
            self.hod_id = "{}{:03d}".format('H', (max_id + 1) if max_id is not None else 1)
        super(HodDetails, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.username



class StaffDetails(models.Model):
    """Database model for staff or teacher in the system"""

    staff_id = models.CharField(_("staff_id"), max_length=200, unique=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    profile_pic = models.FileField(upload_to='staff_profile', null=True, verbose_name='staff profile',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp'])])
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Staff'

    def save(self, *args, **kwargs):
        if not self.staff_id:
            max_id = StaffDetails.objects.aggregate(id_max=Max('id'))['id_max']
            self.staff_id = "{}{:03d}".format('T', (max_id + 1) if max_id is not None else 1)
        super(StaffDetails, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.username


class CourseDetails(models.Model):
    """Database model for courses in the system"""

    course_id = models.CharField(_("course_id"), max_length=200, unique=True, blank=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Course'

    def save(self, *args, **kwargs):
        if not self.course_id:
            max_id = CourseDetails.objects.aggregate(id_max=Max('id'))['id_max']
            self.course_id = "{}{:03d}".format('C', (max_id + 1) if max_id is not None else 1)
        super(CourseDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class StudentDetails(models.Model):
    """Database model for students in the system"""

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    student_id = models.CharField(_("student_id"), max_length=200, unique=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=1,choices= GENDER_CHOICES, blank=True,null=True)
    profile_pic = models.FileField(upload_to='student_profile', null=True, verbose_name='student profile',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp'])])
    admission_year_id = models.ForeignKey(AdmissionYear, on_delete=models.CASCADE)
    course_id = models.ForeignKey(CourseDetails,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Student'

    def save(self, *args, **kwargs):
        if not self.student_id:
            max_id = StudentDetails.objects.aggregate(id_max=Max('id'))['id_max']
            self.student_id = "{}{:03d}".format('S', (max_id + 1) if max_id is not None else 1)
        super(StudentDetails, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.username


class SubjectDetails(models.Model):
    subject_id = models.CharField(_("student_id"), max_length=200, unique=True, blank=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(CourseDetails, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(StaffDetails, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subject'

    def save(self, *args, **kwargs):
        if not self.subject_id:
            max_id = SubjectDetails.objects.aggregate(id_max=Max('id'))['id_max']
            self.subject_id = "{}{:03d}".format('Sub', (max_id + 1) if max_id is not None else 1)
        super(SubjectDetails, self).save(*args, **kwargs)


    def __str__(self):
        return self.subject_name