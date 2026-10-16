from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# Username ပြောင်းရန် Form
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ကိုယ်ရေးအချက်အလက်များအတွက် Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bc_no', 'rank', 'name', 'unit','location','command','military_command', 'phone_number', 'address']
        widgets = {
            'bc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),          # တပ်
            'location': forms.TextInput(attrs={'class': 'form-control'}),      # တည်နေရာ
            'command': forms.TextInput(attrs={'class': 'form-control'}),
            'military_command': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }