from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.unit_list, name='unit_list'),
    path('add/', views.unit_add, name='unit_add'),
    path('update/<int:pk>/', views.unit_update, name='unit_update'),
    path('delete/<int:pk>/', views.unit_delete, name='unit_delete'),
    path('clear/', views.unit_clear, name='unit_clear'),
    # 1. အကောင့်ဝင်ရန် (Login) URL
    path('Login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', views.login_view, name='login'),
    # 2. အကောင့်ထွက်ရန် (Logout) URL (ထွက်ပြီးပါက unit_list သို ပြန်သွားမည်)
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_edit_view, name='profile_edit'),
    #path('password-change/', views.password_change_view, name='password_change'),
    path('profile/', views.home_view, name='profile_edit'),
    # တပ်ဖွဲ့ဝင်များ စာရင်းပြရန် URL
    path('members/', views.profile_list_view, name='profile_list'),

    # တစ်ယောက်ချင်းစီ၏ အသေးစိတ်စာမျက်နှာအတွက် URL
    path('member/<int:pk>/', views.profile_detail_view, name='profile_detail'),


]