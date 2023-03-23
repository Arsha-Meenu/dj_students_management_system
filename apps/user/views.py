from django.shortcuts import render,reverse,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,DeleteView,View,FormView
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import (User,Student,Academics,Course,Department,SubjectAllocation,StudentTakenSubject,
                    Institute,Semester,Classes,Subject,Teacher,UploadFiles)
from .forms import (UserForm,StudentUserForm,CourseForm,DepartmentForm,SubjectAllocationForm,
                    SemesterForm,AcademicsForm,ClassesForm,SubjectsForm,UploadFilesForm,TeacherForm)
from django.shortcuts import get_object_or_404

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm
    fields = "__all__"

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.user.user_type == 1:
            messages.success(self.request, f"{self.request.user.username} logged in successfully. ")
            return redirect('dashboard')
        elif self.request.user.user_type == 2:
            messages.success(self.request, f"{self.request.user.username} logged in successfully. ")
            return redirect('student-dashboard')
        else:
            messages.success(self.request, f"{self.request.user.username} logged in successfully. ")
            return redirect('lecturer-dashboard')


class DashboardView(TemplateView):
    template_name = 'administrator/admin_dashboard.html'

    def get(self,request):
        lecturers = User.objects.filter(user_type = 3).all().count()
        students = Student.objects.all().count()
        courses = Course.objects.all().count()

        context = {
            'lecturers': lecturers,
            'students' :students,
            'courses':courses
        }
        return render(request,'administrator/admin_dashboard.html',context = context)


class StudentDashboardView(TemplateView):
    template_name = 'student/student_dashboard.html'

    def get(self,request):
        student = Student.objects.filter(user = request.user)
        if student:
            department = student.values('department_id', 'department__title','department__course__course_title','department__course_id').first()
            subjects = Subject.objects.filter(course_id =department['department__course_id'] ,department_id=department['department_id']).count()
            department_name = department.get('department__title')
            course_name = department.get('department__course__course_title')
        else:
            department_name = 0
            subjects = 0
            course_name = 0
        context = {
            'subjects':subjects,
            'department':department_name,
            'course_name':course_name
        }
        return render(request, 'student/student_dashboard.html', context=context)

class LecturerDashboardView(View):
    def get(self,request):
        teacher = Teacher.objects.filter(user = request.user)
        if teacher:
            department = teacher.values('department_id', 'department__title','department__course__course_title').first()
            print('dept',department)
            subjects = Subject.objects.filter(department_id=department['department_id']).count()
            department_name = department.get('department__title')
            course_name = department.get('department__course__course_title')
        else:
            department_name = 0
            subjects = 0
            course_name = 0
        context = {
            'subjects':subjects,
            'department':department_name,
            'course_name':course_name
        }
        return render(request, 'lecturer/lecturer_dashboard.html', context=context)

class InstituteInfoView(TemplateView):
    template_name = 'administrator/institute_info.html'

    def get_context_data(self, **kwargs):
        context = super(InstituteInfoView, self).get_context_data(**kwargs)
        context['institute_details'] = Institute.objects.filter(user__user_type = 1).all()
        return context



class ProfileView(TemplateView):
    template_name = 'administrator/admin_profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.filter(id = self.request.user.id).first()
        if user.profile_image:
            profile = user.profile_image
        else:
            profile = request.path
        context = {
            'id': user.id,
            'username':user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'fullname': user.get_full_name,
            'email':user.email,
            'phone':user.mobile_number,
            'address':user.address,
            'profile':profile,
            'date_joined':user.date_joined,
            'user_type':user.get_user_type_display()

        }
        return render(request,'administrator/admin_profile.html',context)


class UpdateProfileView(UpdateView):
    model = User
    form_class = UserForm
    # fields = ['username','email','mobile_number','first_name','last_name','address','profile_image']  # fields / if you want to select all fields, use "__all__"
    template_name = 'administrator/update_profile.html'  # templete for updating
    success_url = '/profile/'


# lecturer views
class LecturerProfileView(View):
    def get(self,request, *args, **kwargs):
        teacher = Teacher.objects.filter(id = kwargs['pk']).first()
        if request.user.id == kwargs['pk']:
            return redirect('/profile/')
        else:
            if teacher.user.profile_image:
                profile = teacher.user.profile_image
            else:
                profile = request.path
            context = {
                'id': teacher.user.id,
                'username':teacher.user.username,
                'firstname': teacher.user.first_name,
                'lastname': teacher.user.last_name,
                'fullname': teacher.user.get_full_name,
                'email':teacher.user.email,
                'phone':teacher.user.mobile_number,
                'address':teacher.user.address,
                'profile':profile,
                'course': teacher.course,
                'department': teacher.department,
                'date_joined':teacher.user.date_joined,
                'user_type':teacher.user.get_user_type_display()

            }
            return render(request,'lecturer/lecturer_profile.html',context)


class LecturerListView(ListView):
    template_name = 'lecturer/lecturer_list.html'
    model = Teacher
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__user_type='3')


class LecturerCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form_class': UserForm(),'teacher_form':TeacherForm()}
        return render(request, 'lecturer/create_lecturer.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, request.FILES)
        teacher_form = TeacherForm(request.POST, request.FILES)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.user_type = 3
            user.save()
            student = teacher_form.save(commit=False)
            student.user_id= user.id
            student.save()
            return HttpResponseRedirect(reverse('lecturer-list'))
        return render(request, 'lecturer/create_lecturer.html', {'form_class': user_form,'teacher_form':teacher_form})


    def get_initial(self):
        intitial_data = super(LecturerCreateView,self).get_initial()
        intitial_data['user_type'] = 3
        return intitial_data


class UpdateLecturerView(UpdateView):
    # model = User
    # form_class = UserForm
    # template_name = 'lecturer/create_lecturer.html'  # template for updating
    # success_url = '/lecturer/list'

    model = User
    second_model = Teacher
    teacher_form = TeacherForm
    form_class = UserForm
    template_name = 'lecturer/create_lecturer.html'
    success_url = "/lecturer/list"

    def get_context_data(self, **kwargs):
        context = super(UpdateLecturerView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        teacher = self.second_model.objects.get(id=pk)
        user = self.model.objects.get(id=teacher.user.id)
        if 'form_class' not in context:
            context['form_class'] = self.form_class(instance=user)
        if 'teacher_form' not in context:
            context['teacher_form'] = self.teacher_form(instance=teacher)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        teacher_id = kwargs['pk']
        teacher = self.second_model.objects.get(id=teacher_id)
        user = self.model.objects.get(id=teacher.user.id)
        teacher_form = self.teacher_form(request.POST, instance=teacher)
        form_class = self.form_class(request.POST, request.FILES, instance=user)

        if teacher_form.is_valid() and form_class.is_valid():
            teacher_form.save()
            form_class.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form_class=form_class, teacher_form=teacher_form))




class DeleteLecturerView(DeleteView):
    model = Teacher
    template_name = 'lecturer/delete_lecturer.html'
    success_url = "/lecturer/list"


class LecturerSubjectListView(ListView):
    template_name = 'lecturer/lecturer_courses.html'
    model = Subject

    def get_context_data(self):
        teacher = Teacher.objects.filter(user=self.request.user)
        if teacher:
            teacher = teacher.values('id','department_id', 'department__title').first()
            print('teac',teacher)
            taken_subjects = SubjectAllocation.objects.filter(lecturer=teacher['id']).filter(subject__department_id=teacher['department_id'])
            print('subj',taken_subjects)
            t = ()
            for i in taken_subjects:
                t += (i.subject.pk,)
        else:
            taken_subjects = 0
        context = {
            'taken_subjects':taken_subjects
        }
        return context



class LecturerSingleSubjectView(TemplateView):
    template_name = 'lecturer/subject_single.html'

    def get_context_data(self, **kwargs):
        files = UploadFiles.objects.filter(subject = kwargs['pk'])
        subject = Subject.objects.filter(id = kwargs['pk'] ).first()
        context = {
            'files':files,
            'subject':subject
        }
        return context

class FileUploadView(View):
    def get(self,request, *args, **kwargs):
        form = UploadFilesForm()
        subject = Subject.objects.filter(id = kwargs['pk']).first()
        context = {
            'subject': subject,
            'form':form
        }
        return render(request, 'lecturer/upload_file_form.html', context)

    def post(self,request, *args, **kwargs):
        subject = Subject.objects.filter(id=kwargs['pk']).first()
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('title') + ' has been uploaded.'))
            return redirect('lecturer-single-subject',pk = subject.id )

class UpdateFileView(View):
    def get(self,request, *args, **kwargs):
        subject = Subject.objects.filter(subject_code = kwargs['subject_code']).first()
        instance = UploadFiles.objects.filter(id=kwargs['file_id']).first()
        form = UploadFilesForm(instance=instance)
        context = {
            'subject': subject,
            'form':form
        }
        return render(request, 'lecturer/upload_file_form.html', context)

    def post(self,request, *args, **kwargs):
        subject = Subject.objects.filter(subject_code = kwargs['subject_code']).first()
        instance = UploadFiles.objects.filter(id = kwargs['file_id']).first()
        form = UploadFilesForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(self.request, (self.request.POST.get('title') + ' has been updated.'))
            return redirect('lecturer-single-subject',pk = subject.id )

class DeleteFileView(DeleteView):
    model = UploadFiles
    template_name = 'lecturer/file_delete.html'

    def get_success_url(self, **kwargs):
        return reverse('lecturer-single-subject', args=(self.object.subject.id,))







# students view

class StudentProfileView(View):
    def get(self,request, *args, **kwargs):
        student = Student.objects.filter(id = kwargs['pk']).first()
        if request.user.id == kwargs['pk']:
            return redirect('/profile/')
        else:
            if student.user.profile_image:
                profile = student.user.profile_image
            else:
                profile = request.path
            context = {
                'id': student.user.id,
                'username':student.user.username,
                'firstname': student.user.first_name,
                'lastname': student.user.last_name,
                'fullname': student.user.get_full_name,
                'email':student.user.email,
                'phone':student.user.mobile_number,
                'address':student.user.address,
                'profile':profile,
                'date_joined':student.user.date_joined,
                'user_type':student.user.get_user_type_display(),
                'course':student.course,
                'department': student.department,
                'timeperiod':student.academic_year

            }
            return render(request,'student/student_profile.html',context)


class StudentSubjectListView(ListView):
    template_name = 'student/student_courses.html'
    model = Course

    def get_context_data(self):
        student = Student.objects.filter(user=self.request.user)
        if student:
            student = student.values('department_id', 'department__title').first()
            subjects = Subject.objects.filter(department_id=student['department_id'])
            taken_subjects = StudentTakenSubject.objects.filter(student__user=self.request.user).filter(subject__department_id=student['department_id'])
            t = ()
            for i in taken_subjects:
                t += (i.subject.pk,)
            subjects = subjects.exclude(id__in=t)
        else:
            subjects = 0
            taken_subjects = 0
        context = {
            'subjects':subjects,
            'taken_subjects':taken_subjects
        }
        return context


class StudentAddSubjectView(CreateView):
    template_name = 'student/student_courses.html'
    queryset = Subject.objects.all()

    def post(self,request):
        ids = ()
        data = self.request.POST.getlist('subject')
        for key in data:
            ids = ids + (str(key),)
            print('s', ids)
        for s in range(0, len(ids)):
            student = Student.objects.get(user = request.user.id)
            subject = Subject.objects.get(subject_code=ids[s])
            obj = StudentTakenSubject.objects.create(student=student, subject=subject)
            obj.save()
        return redirect('student-subject-list')


class StudentDropSubjectView(View):
    def post(self,request):
        ids=()
        data = self.request.POST.getlist('taken_subject')
        for key in data:
            ids = ids+(str(key),)
            print('ids',ids)
        for s in range(0,len(ids)):
            student = Student.objects.get(user=request.user.id)
            subject = Subject.objects.get(subject_code=ids[s])
            obj = StudentTakenSubject.objects.get(student=student, subject=subject)
            obj.delete()
        return redirect('student-subject-list')

class StudentListView(ListView):
    template_name = 'student/students_list.html'
    model = Student

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__user_type='2')


class CreateStudentView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'user_form': UserForm(),'student_form':StudentUserForm()}
        return render(request, 'student/create_student.html', context)


    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, request.FILES)
        student_form = StudentUserForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.user_type = 2
            user.save()
            student = student_form.save(commit=False)
            student.user_id= user.id
            student.save()
            return HttpResponseRedirect(reverse('student-list'))
        return render(request, 'student/create_student.html', {'user_form': user_form,'student_form':student_form})


class UpdateStudentView(UpdateView):
    model = Student
    second_model = User
    form_class = StudentUserForm
    second_form_class = UserForm
    template_name = 'student/student_update.html'
    success_url = "/student/list"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        student = self.model.objects.get(id = pk)
        user = self.second_model.objects.get(id = student.user.id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance= user)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        student_id = kwargs['pk']
        student = self.model.objects.get(id = student_id)
        user = self.second_model.objects.get(id = student.user.id)
        form = self.form_class(request.POST, instance=student)
        form2 = self.second_form_class(request.POST, request.FILES, instance=user)

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form =form,form2 =form2))

class DeleteStudentView(DeleteView):
    model = Student
    template_name = 'student/delete_student.html'
    success_url = "/student/list"


# department
class CoursesListView(TemplateView):
    template_name = 'departments and course/courses_list.html'

    def get(self, request):
        course = Course.objects.all()

        context = {
            'courses': course
        }
        return render(request, 'departments and course/courses_list.html', context=context)

class CourseCreateView(CreateView):
    template_name = 'departments and course/create_course.html'
    form_class = CourseForm
    success_url = "/courses/list"

    def form_valid(self, form):
        model = form.save(commit = False)
        return super().form_valid(form)

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'departments and course/create_course.html'
    success_url = '/courses/list'


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'departments and course/delete_course.html'
    success_url = "/courses/list"

# Courses

class DepartmentListView(TemplateView):
    template_name = 'departments and course/departments_list.html'

    def get(self, request,**kwargs):
        department = Department.objects.filter(course_id = self.kwargs['pk']).all()

        context = {
            'departments': department,
            'course_id':self.kwargs['pk']
        }
        return render(request, 'departments and course/departments_list.html', context=context)

class DepartmentCreateView(CreateView):
    template_name = 'departments and course/create_department.html'
    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        course = Course.objects.filter(id = self.kwargs.get('pk')).first()
        context = super().get_context_data(**kwargs)
        context['course'] = course
        context['course_id'] = course.id
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        model = form.save(commit = False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        department = Department.objects.filter(id=self.object.id).values('course').first()
        return reverse("department-list", kwargs={'pk': department['course']})


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments and course/create_department.html'


    def get_context_data(self, **kwargs):
        department = Department.objects.filter(id = self.kwargs.get('pk')).values('course__course_title','course').first()
        context = super().get_context_data(**kwargs)
        context['course'] = department['course__course_title']
        context['course_id'] = department['course']
        return context


    def get_success_url(self, **kwargs):
        department = Department.objects.filter(id = self.object.id).values('course__course_title','course').first()
        return reverse("department-list", kwargs={'pk': department['course']})

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'departments and course/delete_department.html'
    def get_success_url(self, **kwargs):
        return reverse("department-list", kwargs={'pk':  self.object.course.id})


class AllocatedSubjectListView(ListView):
    template_name = 'departments and course/allocated_subject_list.html'
    model = SubjectAllocation
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class SubjectAllocationCreateView(CreateView):
    template_name = 'departments and course/subject_allocation_teacher.html'
    form_class = SubjectAllocationForm
    model = SubjectAllocation

    def form_valid(self, form):
        print('valid')
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        print('success')
        return reverse("allocated-subjects-list")


class AllocatedSubjectUpdateView(UpdateView):
    model = SubjectAllocation
    form_class = SubjectAllocationForm
    template_name = 'departments and course/subject_allocation_teacher.html'

    def get_success_url(self, **kwargs):
        return reverse("allocated-subjects-list")

class AllocatedSubjectDeleteView(DeleteView):
    model = SubjectAllocation
    template_name = 'departments and course/allocated_subject_delete.html'
    def get_success_url(self, **kwargs):
        return reverse("allocated-subjects-list")

#semester
class SemesterListView(ListView):
    template_name = 'semester/semester_list.html'
    queryset = Semester.objects.all()

class SemesterCreateView(CreateView):
    template_name = 'semester/semester_create.html'
    form_class = SemesterForm

    def form_valid(self, form):
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("semester-list")


class SemesterUpdateView(UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'semester/semester_update.html'

    def get_success_url(self, **kwargs):
        return reverse("semester-list")
#
class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'semester/semester_delete.html'
    def get_success_url(self, **kwargs):
        return reverse("semester-list")

# academic year
class AcademicsListView(ListView):
    template_name = 'academic_year/academics_list.html'
    queryset = Academics.objects.all()


class AcademicsCreateView(CreateView):
    template_name = 'academic_year/create_academics.html'
    form_class = AcademicsForm

    def form_valid(self, form):
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("academic-list")


class AcademicsUpdateView(UpdateView):
    model = Academics
    form_class = AcademicsForm
    template_name = 'academic_year/academics_update.html'

    def get_success_url(self, **kwargs):
        return reverse("academic-list")
#
class AcademicsDeleteView(DeleteView):
    model = Academics
    template_name = 'academic_year/delete_academics.html'
    def get_success_url(self, **kwargs):
        return reverse("academic-list")


# classes

class ClassesListView(ListView):
    template_name = 'classes/classes_list.html'
    queryset = Classes.objects.all()


class ClassesCreateView(CreateView):
    template_name = 'classes/classes_create.html'
    form_class = ClassesForm

    def form_valid(self, form):
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("classes-list")


class ClassesUpdateView(UpdateView):
    model = Classes
    form_class = ClassesForm
    template_name = 'classes/classes_update.html'

    def get_success_url(self, **kwargs):
        return reverse("classes-list")
#
class ClassesDeleteView(DeleteView):
    model = Classes
    template_name = 'classes/delete_classes.html'
    def get_success_url(self, **kwargs):
        return reverse("classes-list")


# subjects

class SubjectsListView(ListView):
    template_name = 'subjects/subject_list.html'
    queryset = Subject.objects.all()


class SubjectCreateView(CreateView):
    template_name = 'subjects/subject_create.html'
    form_class = SubjectsForm

    def form_valid(self, form):
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("subjects-list")


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectsForm
    template_name = 'subjects/subject_update.html'

    def get_success_url(self, **kwargs):
        return reverse("subjects-list")
#
class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subjects/delete_subject.html'
    def get_success_url(self, **kwargs):
        return reverse("subjects-list")


