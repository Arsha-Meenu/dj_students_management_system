from django.shortcuts import render,redirect
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import HodDetails,StaffDetails,StudentDetails,SubjectDetails,CourseDetails,Attendance,StudentAttendanceReport,StudentLeaveReport,StaffLeaveReport

class HomePageView(TemplateView):
    template_name = 'hod/create_staff.html'


class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        # Process the request if posted data are available
        email = request.POST['email']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(email = email,password = password)
        if user != None:
            login(request,user) # Save session as cookie to login the user
            return render(request,'hod/dashboard.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            messages.error(request, "Incorrect email or/and password")
            return render(request,self.template_name)

class AdminDashboardView(View):
    def get(self, request):
        course_data = CourseDetails.objects.all()
        student_data = StudentDetails.objects.all()
        subject_data = SubjectDetails.objects.all()
        staff_data = StaffDetails.objects.all()

        #Total Data and Students and Staff Chart
        total_staff_count = staff_data.count()
        total_students_count = student_data.count()
        total_course_count = course_data.count()
        total_subject_count = subject_data.count()

        # Total Students/Subjects in Each Course Chart
        courses_name_list = []
        students_course_list = []
        subjects_course_list = []
        for course in course_data:
            courses_name_list.append(course.course_name)
            subjects_course = SubjectDetails.objects.filter(course_id = course.id).count()
            subjects_course_list.append(subjects_course)
            students_course = StudentDetails.objects.filter(course_id = course.id).count()
            students_course_list.append(students_course)

        # Total students in each subjects
        subject_name = []
        students_count = []
        for subject in subject_data:
            subject_name.append(subject.subject_name)
            courses = CourseDetails.objects.filter(id = subject.course_id.id).values('id')
            for i in courses:
                students = StudentDetails.objects.filter(course_id = i['id']).count()
                students_count.append(students)

        # students attendance vs leave
        students_name_list = []
        student_present_list = []
        student_absent_list = []
        for student in student_data:
            students_name_list.append(student.user.username)
            student_present = StudentAttendanceReport.objects.filter(student_id = student.id,status = True).count()
            student_present_list.append(student_present)
            student_absent = StudentAttendanceReport.objects.filter(student_id = student.id,status = False).count()
            student_leaves = StudentLeaveReport.objects.filter(student_id = student.id,status = 1).count()
            student_absent_list.append(student_leaves+student_absent)


        # staff attendance vs leave
        staffs_name_list = []
        staff_present_list = []
        staff_leave_list = []
        for staff in staff_data:
            staffs_name_list.append(staff.user.username)
            subject = SubjectDetails.objects.filter(staff_id = staff.id)
            staff_attendance = Attendance.objects.filter(subject_id__in = subject).count()
            staff_present_list.append(staff_attendance)
            staff_leave = StaffLeaveReport.objects.filter(staff_id = staff.id,status=1).count()
            staff_leave_list.append(staff_leave)


        data = {
            # total data
            'total_students': total_students_count,
            'total_staffs': total_staff_count,
            'total_courses': total_course_count,
            'total_subjects': total_subject_count,
            # pie and doughnut chart data
            'subjects_course':subjects_course_list,
            'students_course':students_course_list,
            'courses_name_list':courses_name_list,
            'subject_name':subject_name,
            'students_count':students_count,
            # bar graph
            'students_name_list':students_name_list,
            'student_present':student_present_list,
            'student_leave':student_absent_list,
            'staff_present':staff_present_list,
            'staff_leave':staff_leave_list,
            'staffs_name_list':staffs_name_list
        }
        return render(request, 'hod/dashboard.html', context=data)

class AdminManageStaffView(TemplateView):
    template_name = 'hod/manage_staff.html'

