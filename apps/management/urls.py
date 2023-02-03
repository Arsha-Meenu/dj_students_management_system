from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name = 'home-page-view'),
    path('login/',views.LoginView.as_view(),name = 'user_login'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-manage-staff/', views.ManageStaffView.as_view(), name='admin-manage-staff'),
    path('create-staff/', views.CreateStaffView.as_view(), name='create-staff'),
    path('update-staff/<int:pk>', views.UpdateStaffView.as_view(), name='update-staff'),
    path('delete-staff/<int:pk>', views.DeleteStaffView.as_view(), name='delete-staff'),

]