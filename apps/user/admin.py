from django.contrib import admin
from .models import User,Student,Course,TimePeriod


admin.site.register(User)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id','user','course_id']
admin.site.register(Student,StudentAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_name']
admin.site.register(Course,CourseAdmin)

admin.site.register(TimePeriod)

