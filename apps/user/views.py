from django.shortcuts import render,reverse,redirect,HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,DeleteView,View
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import User,Student,TimePeriod,Course,Program,CourseAllocation
from .forms import UserForm,StudentUserForm,CourseForm,ProgramForm,CourseAllocationForm
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
            return super(UserLoginView, self).form_valid(form)


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
        department = Student.objects.filter(user = request.user).values('department_id','department__title').first()
        courses = Course.objects.filter(department_id=department['department_id']).count()
        context = {
            'courses':courses,
            'department':department.get('department__title')
        }
        return render(request, 'student/student_dashboard.html', context=context)


class ProfileView(TemplateView):
    template_name = 'administrator/admin_profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.filter(id = self.request.user.id).first()
        if user.profiles:
            profile = user.profiles
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
    # fields = ['username','email','mobile_number','first_name','last_name','address','profiles']  # fields / if you want to select all fields, use "__all__"
    template_name = 'administrator/update_profile.html'  # templete for updating
    success_url = '/profile/'


# lecturer views
class LecturerProfileView(View):
    def get(self,request, *args, **kwargs):
        user = User.objects.filter(id = kwargs['pk']).first()
        if request.user.id == kwargs['pk']:
            return redirect('/profile/')
        else:
            if user.profiles:
                profile = user.profiles
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
            return render(request,'lecturer/lecturer_profile.html',context)


class LecturerListView(ListView):
    template_name = 'lecturer/lecturer_list.html'
    model = User
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_type='3')


class LecturerCreateView(CreateView):
    template_name = 'lecturer/create_lecturer.html'
    form_class = UserForm
    success_url = "/lecturer/list"

    def form_valid(self, form):
        model = form.save(commit = False)
        model.user_type = 3
        model.save()
        return super().form_valid(form)

    def get_initial(self):
        intitial_data = super(LecturerCreateView,self).get_initial()
        intitial_data['user_type'] = 3
        return intitial_data


class UpdateLecturerView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'lecturer/create_lecturer.html'  # template for updating
    success_url = '/lecturer/list'


class DeleteLecturerView(DeleteView):
    model = User
    template_name = 'lecturer/delete_lecturer.html'
    success_url = "/lecturer/list"


# students view

class StudentProfileView(View):
    def get(self,request, *args, **kwargs):
        student = Student.objects.filter(id = kwargs['pk']).first()
        if request.user.id == kwargs['pk']:
            return redirect('/profile/')
        else:
            if student.user.profiles:
                profile = student.user.profiles
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
                'departments and course':student.course,
                'timeperiod':student.period

            }
            return render(request,'student/student_profile.html',context)


class StudentCourseListView(ListView):
    template_name = 'student/student_courses.html'
    model = Course

    def get_queryset(self):
        department = Student.objects.filter(user=self.request.user).values('department_id', 'department__title').first()
        courses = Course.objects.filter(department_id=department['department_id'])
        return courses

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


# programs
class ProgramsListView(TemplateView):
    template_name = 'departments and course/programs_list.html'

    def get(self, request):
        programs = Program.objects.all()

        context = {
            'programs': programs
        }
        return render(request, 'departments and course/programs_list.html', context=context)

class ProgramCreateView(CreateView):
    template_name = 'departments and course/create_program.html'
    form_class = ProgramForm
    success_url = "/programs/list"

    def form_valid(self, form):
        model = form.save(commit = False)
        return super().form_valid(form)

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'departments and course/create_program.html'
    success_url = '/programs/list'


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'departments and course/delete_program.html'
    success_url = "/programs/list"

# Courses

class CoursesListView(TemplateView):
    template_name = 'departments and course/courses_list.html'

    def get(self, request,**kwargs):
        courses = Course.objects.filter(department_id = self.kwargs['pk']).all()
        context = {
            'courses': courses
        }
        return render(request, 'departments and course/courses_list.html', context=context)

class CourseCreateView(CreateView):
    template_name = 'departments and course/create_course.html'
    form_class = CourseForm


    def form_valid(self, form):
        model = form.save(commit = False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("courses-list", kwargs={'pk': self.object.department.id})

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'departments and course/create_course.html'

    def get_success_url(self, **kwargs):
        return reverse("courses-list", kwargs={'pk': self.object.department.id})

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'departments and course/delete_course.html'
    def get_success_url(self, **kwargs):
        return reverse("courses-list", kwargs={'pk': self.object.department.id})


class AllocatedCoursesListView(ListView):
    template_name = 'departments and course/allocated_courses_list.html'
    model = CourseAllocation
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CourseAllocationView(CreateView):
    template_name = 'departments and course/course_allocation.html'
    form_class = CourseAllocationForm

    def form_valid(self, form):
        model = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("allocated-courses-list")


class AllocatedCoursesUpdateView(UpdateView):
    model = CourseAllocation
    form_class = CourseAllocationForm
    template_name = 'departments and course/course_allocation.html'

    def get_success_url(self, **kwargs):
        return reverse("allocated-courses-list")

class AllocatedCoursesDeleteView(DeleteView):
    model = CourseAllocation
    template_name = 'departments and course/allocated_course_delete.html'
    def get_success_url(self, **kwargs):
        return reverse("allocated-courses-list")