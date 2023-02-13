from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name = 'login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('logout/',LogoutView.as_view(next_page = 'login'), name='logout'),
    path('profile/',views.ProfileView.as_view(), name='profile'),

]