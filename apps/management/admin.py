from django.contrib import admin
from .models import User,HodDetails,StaffDetails,StudentDetails,CourseDetails,SubjectDetails


admin.site.register(User)
admin.site.register(HodDetails)

class StaffDetailsAdmin(admin.ModelAdmin):
    list_display = ['staff_id','user']
admin.site.register(StaffDetails,StaffDetailsAdmin)

class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ['student_id','user','course_id']
admin.site.register(StudentDetails,StudentDetailsAdmin)

class CourseDetailsAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_name']
admin.site.register(CourseDetails,CourseDetailsAdmin)

class SubjectDetailsAdmin(admin.ModelAdmin):
    list_display = ['subject_id','subject_name','course_id','staff_id']
admin.site.register(SubjectDetails,SubjectDetailsAdmin)
