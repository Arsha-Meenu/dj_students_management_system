from django.contrib import admin
from .models import User,Student,Course,TimePeriod,Program,CourseAllocation


admin.site.register(User)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id','user','course_id']
admin.site.register(Student,StudentAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id','title']
admin.site.register(Course,CourseAdmin)

admin.site.register(TimePeriod)
admin.site.register(Program)
admin.site.register(CourseAllocation)

