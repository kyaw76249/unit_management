from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [

    path('', views.unit_list, name='unit_list'),
    path('add/', views.unit_add, name='unit_add'),
    path('update/<int:pk>/', views.unit_update, name='unit_update'),
    path('delete/<int:pk>/', views.unit_delete, name='unit_delete'),
    path('clear/', views.unit_clear, name='unit_clear'),
    # 1. အကောင့်ဝင်ရန် (Login) URL
    path('login/', auth_views.LoginView.as_view(template_name='units_app/login.html'), name='login'),
    # 2. အကောင့်ထွက်ရန် (Logout) URL (ထွက်ပြီးပါက unit_list သို ပြန်သွားမည်)
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_edit_view, name='profile_edit'),
    path('password-change/', views.password_change_view, name='password_change'),


]