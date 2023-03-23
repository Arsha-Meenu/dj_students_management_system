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
    path('institute/info',views.InstituteInfoView.as_view(),name = 'institute-info'),

    # lecturer
    path('lecturer/dashboard/', views.LecturerDashboardView.as_view(), name='lecturer-dashboard'),
    path('lecturer/list', views.LecturerListView.as_view(), name='lecturer-list'),
    path('lecturer/create', views.LecturerCreateView.as_view(), name='lecturer-create'),
    path('lecturer/edit/<int:pk>/', views.UpdateLecturerView.as_view(), name='lecturer-update'),
    path('lecturer/delete/<int:pk>/', views.DeleteLecturerView.as_view(), name='lecturer-delete'),
    path('lecturer/profile/<int:pk>/', views.LecturerProfileView.as_view(), name='lecturer-profile'),
    path('lecturer/subject/list/', views.LecturerSubjectListView.as_view(), name='lecturer-subject-list'),
    path('lecturer/single/subject/<int:pk>/', views.LecturerSingleSubjectView.as_view(), name='lecturer-single-subject'),
    path('subject/file/upload/<int:pk>/', views.FileUploadView.as_view(), name='file-upload-view'),
    path('subject/<slug:subject_code>/file/update/<int:file_id>/', views.UpdateFileView.as_view(), name='file-update-view'),
    path('subject/file/delete/<int:pk>/', views.DeleteFileView.as_view(),name='file-delete-view'),

    # students
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student-dashboard'),
    path('student/list', views.StudentListView.as_view(), name='student-list'),
    path('student/create', views.CreateStudentView.as_view(), name='student-create'),
    path('student/edit/<int:pk>/', views.UpdateStudentView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', views.DeleteStudentView.as_view(), name='student-delete'),
    path('student/profile/<int:pk>/', views.StudentProfileView.as_view(), name='student-profile'),
    path('student/subject/list/', views.StudentSubjectListView.as_view(), name='student-subject-list'),
    path('student/add/subject/', views.StudentAddSubjectView.as_view(), name='student-add-subject'),
    path('student/drop/subject/', views.StudentDropSubjectView.as_view(), name='student-drop-subject'),

    # programs and courses
    path('department/list/<int:pk>/',views.DepartmentListView.as_view(),name = 'department-list'),
    path('department/create/<int:pk>/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('department/edit/<int:pk>/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('department/delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='department-delete'),
    path('courses/list',views.CoursesListView.as_view(),name = 'courses-list'),
    path('course/create', views.CourseCreateView.as_view(), name='course-create'),
    path('course/edit/<int:pk>/', views.CourseUpdateView.as_view(), name='course-update'),
    path('course/delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course-delete'),

    # subject allocated to lecturers
    path('allocated-subjects/list/', views.AllocatedSubjectListView.as_view(), name='allocated-subjects-list'),
    path('subjects/allocation', views.SubjectAllocationCreateView.as_view(), name='subjects-allocation'),
    path('allocated-subject/edit/<int:pk>/', views.AllocatedSubjectUpdateView.as_view(), name='allocated-subject-update'),
    path('allocated-subject/delete/<int:pk>/', views.AllocatedSubjectDeleteView.as_view(), name='allocated-subject-delete'),

    #semester setting
    path('semester/list',views.SemesterListView.as_view(),name = 'semester-list'),
    path('semester/create',views.SemesterCreateView.as_view(),name = 'semester-create'),
    path('semester/edit/<int:pk>/', views.SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/delete/<int:pk>/', views.SemesterDeleteView.as_view(), name='semester-delete'),

    #academic year
    path('academic/list', views.AcademicsListView.as_view(), name='academic-list'),
    path('academic/create', views.AcademicsCreateView.as_view(), name='academic-create'),
    path('academic/edit/<int:pk>/', views.AcademicsUpdateView.as_view(), name='academic-update'),
    path('academic/delete/<int:pk>/', views.AcademicsDeleteView.as_view(), name='academic-delete'),

    # classes
    path('class/list', views.ClassesListView.as_view(), name='classes-list'),
    path('class/create', views.ClassesCreateView.as_view(), name='class-create'),
    path('class/edit/<int:pk>/', views.ClassesUpdateView.as_view(), name='class-update'),
    path('class/delete/<int:pk>/', views.ClassesDeleteView.as_view(), name='class-delete'),

    # subjects
    path('subjects/list', views.SubjectsListView.as_view(), name='subjects-list'),
    path('subject/create', views.SubjectCreateView.as_view(), name='subject-create'),
    path('subject/edit/<int:pk>/', views.SubjectUpdateView.as_view(), name='subject-update'),
    path('subject/delete/<int:pk>/', views.SubjectDeleteView.as_view(), name='subject-delete'),
]