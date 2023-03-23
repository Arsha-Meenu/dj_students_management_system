from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.core.validators import FileExtensionValidator


A='A'
B='B'
C='C'
D='D'
E='E'
F='F'

PASS ='PASS'
FAIL = 'FAIL'


GRADE = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
    (D, 'D'),
    (E, 'E'),
    (F, 'F'),
)
REMARK = (
    (PASS, 'PASS'),
    (FAIL, 'FAIL')
)

YEARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    )


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
    profile_image = models.FileField(upload_to='profile_image', null=True, verbose_name='user profile image',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp','pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
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


def get_user_type():
    return User.objects.get(user_type =1)
class Institute(models.Model):
    name = models.CharField(_('Institute Name'),max_length=150, blank=True,null=True)
    user = models.ForeignKey(User,default= get_user_type,on_delete=models.SET_NULL, blank=True,null=True)
    establish =  models.DateTimeField(_('establish'), auto_now_add=True, blank=True,null=True)
    email = models.EmailField(max_length=250, blank=True,null=True)
    website = models.CharField(max_length=250, blank=True,null=True)
    mobile_number = PhoneNumberField(_('Mobile Number'),null=True, blank=True, unique=True)
    telephone = PhoneNumberField(null=True, blank=True, unique=True)
    address = models.TextField(blank=True,null=True)
    logo = models.FileField(upload_to='institute_logo', blank=True,null=True, verbose_name='Institute Logo',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png','avif' ,'webp','pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.name


class Classes(models.Model): # for class
    class_name = models.CharField(max_length=150)
    class_code = models.CharField(max_length=150)
    class_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.class_name

class Course(models.Model): # for department
    BACHELOR_DEGREE = "Bachelor"
    MASTER_DEGREE = "Master"

    LEVEL = (
        (BACHELOR_DEGREE, "Bachelor Degree"),
        (MASTER_DEGREE, "Master Degree"),
    )

    course_code = models.CharField(_("course_code"), max_length=200, unique=True, blank=True)
    course_title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.course_code:
            max_id = Course.objects.aggregate(id_max=Max('id'))['id_max']
            self.course_code = "{}{:03d}".format('C', (max_id + 1) if max_id is not None else 1)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_title

class Faculties(models.Model): # for faculty
    faculty_code = models.CharField(max_length=150, unique=True)
    faculty_name = models.CharField(max_length=150)
    faculty_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.faculty_name


class Session(models.Model):
    session = models.CharField( max_length=200, unique=True, blank=True)
    is_current_session = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.session

class Semester(models.Model):
    semester_code = models.CharField(_("semester_code"), max_length=200, unique=True)
    semester_name = models.CharField(max_length=150)
    semester_duration = models.CharField(max_length=100)
    # session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    is_current_semester = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.semester_name


class Department(models.Model):
    department_id = models.CharField(_("department_id"), max_length=200, unique=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    faculty  = models.ForeignKey(Faculties,on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.department_id:
            max_id = Department.objects.aggregate(id_max=Max('id'))['id_max']
            self.department_id = "{}{:03d}".format('D', (max_id + 1) if max_id is not None else 1)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Academics(models.Model):
    academic_year = models.CharField(max_length=50)
    academic_status = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return str(self.academic_year)

    # def __str__(self):
    #     return str(self.start_year)  + " --- " + str(self.end_year)


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    student_id = models.CharField(_("student_id"), max_length=200, unique=True, blank=True)
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Academics,on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            max_id = Student.objects.aggregate(id_max=Max('id'))['id_max']
            self.student_id = "{}{:03d}".format('S', (max_id + 1) if max_id is not None else 1)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):#for teacher
    teacher_code = models.CharField(_("teacher_code"), max_length=200, unique=True, blank=True)
    user  = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey(Faculties,on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.teacher_code:
            max_id = Teacher.objects.aggregate(id_max=Max('id'))['id_max']
            self.teacher_code = "{}{:03d}".format('T', (max_id + 1) if max_id is not None else 1)
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username



class Subject(models.Model):
    subject_code = models.CharField(_("subject_code"), max_length=200, unique=True, blank=True)
    subject_name = models.CharField(max_length=150)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    is_elective = models.BooleanField(default=False, blank=True, null=True)
    credit = models.IntegerField(null=True, default=0)
    year = models.ForeignKey(Academics, on_delete=models.SET_NULL, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)


    def save(self, *args, **kwargs):
        if not self.subject_code:
            max_id = Subject.objects.aggregate(id_max=Max('id'))['id_max']
            self.subject_code = "{}{:03d}".format('S', (max_id + 1) if max_id is not None else 1)
        super(Subject, self).save(*args, **kwargs)



    def __str__(self):
        return self.subject_name


class StudentTakenSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='taken_subjects')
    def __str__(self):
        return "{0} ({1})".format(self.subject.subject_name, self.subject.subject_code)




class SubjectAllocation(models.Model):
    lecturer = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='allocated_lecturer')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, related_name='allocated_subjects')
    def __str__(self):
        return self.lecturer.user.get_full_name

class UploadFiles(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    file = models.FileField(upload_to='subject_files', blank=True,null=True, verbose_name='Subject Files',
                                   validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png','avif' ,'webp','pdf',
                                                                       'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip',
                                                                       'mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return str(self.file)[6:]



class Roll(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=150)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)


    def __str__(self):
        return self.roll_no


