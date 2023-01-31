from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name = 'home-page-view'),
    path('login/',views.LoginView.as_view(),name = 'user_login'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-manage-staff/', views.ManageStaffView.as_view(), name='admin-manage-staff'),
    path('create-staff/', views.CreateStaffView.as_view(), name='create-staff'),

]