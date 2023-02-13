from django.shortcuts import render,reverse,redirect
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import User,Student,TimePeriod,Course

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
    template_name = 'administrator/dashboard.html'

    def get(self,request):
        lecturers = User.objects.filter(user_type = 3).all().count()
        students = Student.objects.all().count()
        courses = Course.objects.all().count()

        context = {
            'lecturers': lecturers,
            'students' :students,
            'courses':courses
        }
        return render(request,'administrator/dashboard.html',context = context)


class ProfileView(TemplateView):
    template_name = 'administrator/profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.filter(id = self.request.user.id).first()
        context = {
            'id': user.id,
            'username':user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'fullname': user.get_full_name,
            'email':user.email,
            'phone':user.mobile_number,
            'address':user.address,
            'profile':user.profiles,
            'date_joined':user.date_joined,
            'user_type':user.get_user_type_display()

        }
        return render(request,'administrator/profile.html',context)

