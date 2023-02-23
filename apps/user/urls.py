from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView

urlpatterns = [
    path('',views.UserLoginView.as_view(),name = 'login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('logout/',LogoutView.as_view(next_page = 'login'), name='logout'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.UpdateProfileView.as_view(), name='profile-edit'),
    # path('profile/password-change', PasswordChangeView.as_view(template_name = 'authentication/change_password.html', success_url = 'profile'),name= 'password-change'),
    # path('password_change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # lecturer
    path('lecturer/list', views.LecturerListView.as_view(), name='lecturer-list'),
    path('lecturer/create', views.LecturerCreateView.as_view(), name='lecturer-create'),
    path('lecturer/edit/<int:pk>/', views.UpdateLecturerView.as_view(), name='lecturer-update'),
    path('lecturer/delete/<int:pk>/', views.DeleteLecturerView.as_view(), name='lecturer-delete'),
    path('lecturer/profile/<int:pk>/', views.LecturerProfileView.as_view(), name='lecturer-profile'),
    # students
    path('student/list', views.StudentListView.as_view(), name='student-list'),
    path('student/create', views.CreateStudentView.as_view(), name='student-create'),
    path('student/edit/<int:pk>/', views.UpdateStudentView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', views.DeleteStudentView.as_view(), name='student-delete'),
    path('student/profile/<int:pk>/', views.StudentProfileView.as_view(), name='student-profile'),
    # courses
    path('courses/list',views.CoursesListView.as_view(),name = 'courses-list'),
    path('course/create', views.CourseCreateView.as_view(), name='course-create'),
    path('course/edit/<int:pk>/', views.CourseUpdateView.as_view(), name='course-update'),
    path('course/delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course-delete'),

]