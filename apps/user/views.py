from django.shortcuts import render,reverse,redirect,HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,DeleteView,View
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import User,Student,TimePeriod,Course
from .forms import UserForm,StudentUserForm
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
            return super(UserLoginView, self).form_valid(form)
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


class ProfileView(TemplateView):
    template_name = 'administrator/admin_profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.filter(id = self.request.user.id).first()
        # image = request.FILES['profiles'] for save an image
        # if image:
        #     filename = FileSystemStorage().save('profile_pics/' + image.name, image)
        #     user.profile_pic = filename
        # user.save()
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
    model = User
    fields = ("user_type","username","email","mobile_number","first_name","last_name","address","profiles")
    success_url = "/lecturer/list"


class UpdateLecturerView(UpdateView):
    model = User
    form_class = UserForm
    # fields = ['username','email','mobile_number','first_name','last_name','address','profiles']  # fields / if you want to select all fields, use "__all__"
    template_name = 'administrator/update_profile.html'  # template for updating
    success_url = '/lecturer/list'


class DeleteLecturerView(DeleteView):
    model = User
    template_name = 'lecturer/delete_lecturer.html'
    success_url = "/lecturer/list"


# students view

class StudentProfileView(View):
    def get(self,request, *args, **kwargs):
        user = Student.objects.filter(user__id = kwargs['pk']).first()
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
            return render(request,'student/student_profile.html',context)


class StudentListView(ListView):
    template_name = 'student/students_list.html'
    model = Student
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CreateStudentView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'user_form': UserForm(),'student_form':StudentUserForm()}
        return render(request, 'student/create_student.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, request.FILES)
        student_form = StudentUserForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.save()
            student = student_form.save()
            student.save()
            return HttpResponseRedirect(reverse('student-list'))
        return render(request, 'student/create_student.html', {'user_form': user_form,'student_form':student_form})


class UpdateStudentView(UpdateView):
    model = Student
    form_class = UserForm
    form_class2 = StudentUserForm
    template_name = 'administrator/update_profile.html'
    success_url = "/student/list"


#     https://stackoverflow.com/questions/61903021/django-class-based-updateview-with-form-for-multiple-uploaded-files
# https://www.google.com/search?q=class+based+update+view+in+django&ei=pbbzY5qvKqnv4-EPyqS3-Aw&oq=cassbased+views+update+method+in+django&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgAMgUIABCiBDIFCAAQogQ6CggAEEcQ1gQQsAM6BwgAEA0QgAQ6CAgAEAgQBxAeOggIABAIEB4QDToFCAAQhgM6CgghEKABEMMEEApKBAhBGABQ6w9YxStgtjloAnABeACAAbABiAGtE5IBBDAuMTaYAQCgAQHIAQjAAQE&sclient=gws-wiz-serp
class DeleteProfileView(DeleteView):
    model = Student
    template_name = 'student/delete_student.html'
    success_url = "/student/list"
