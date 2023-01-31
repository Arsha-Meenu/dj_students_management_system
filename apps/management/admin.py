from django.contrib import admin
from .models import User,HodDetails,StaffDetails,StudentDetails,CourseDetails,SubjectDetails,Attendance,AdmissionYear,StudentAttendanceReport,StudentLeaveReport,StaffLeaveReport


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


class AdmissionYearAdmin(admin.ModelAdmin):
    list_display = ['admission_start_year','admission_end_year']
admin.site.register(AdmissionYear,AdmissionYearAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['attendance_id','attendance_date','subject_id','admission_year_id']
admin.site.register(Attendance,AttendanceAdmin)


class StudentAttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['report_id','student_id','attendance_id','status']
admin.site.register(StudentAttendanceReport,StudentAttendanceReportAdmin)


class StudentLeaveReportAdmin(admin.ModelAdmin):
    list_display = ['report_id','student_id','leave_date','leave_message','status']
admin.site.register(StudentLeaveReport,StudentLeaveReportAdmin)


class StaffLeaveReportAdmin(admin.ModelAdmin):
    list_display = ['report_id','staff_id','leave_date','leave_message','status']
admin.site.register(StaffLeaveReport,StaffLeaveReportAdmin)