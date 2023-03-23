from django.contrib import admin
from .models import User,Student,Course,Academics,Department,SubjectAllocation,StudentTakenSubject,Faculties,Subject,Session,Semester,Teacher,Roll,Institute,UploadFiles


admin.site.register(User)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id','user','academic_year']
admin.site.register(Student,StudentAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code','course_title','description']
admin.site.register(Course,CourseAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code','subject_name','department','course']
admin.site.register(Subject,SubjectAdmin)


class SubjectAllocationAdmin(admin.ModelAdmin):
    list_display = ['lecturer','subject']
admin.site.register(SubjectAllocation,SubjectAllocationAdmin)

class StudentTakenSubjectAdmin(admin.ModelAdmin):
    list_display = ['student','subject']
admin.site.register(StudentTakenSubject,StudentTakenSubjectAdmin)


admin.site.register(Academics)
admin.site.register(Department)
admin.site.register(Session)
admin.site.register(Teacher)
admin.site.register(Semester)
admin.site.register(Roll)
admin.site.register(Faculties)
admin.site.register(Institute)
admin.site.register(UploadFiles)