from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label="နာမည်",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter  Full Name'}),
    )
    email = forms.EmailField(
        required=True,
        label="အီးမေးလ်",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'})
    )
    phone_number = forms.CharField(
        required=False,
        label="ဖုန်းနံပါတ်",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter  Phone Number'}),
    )

class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'email', 'phone_number')

    # Username နဲ့ Password တွေအတွက်ပါ Placeholder လိုချင်ရင် ဒီလိုထည့်နိုင်ပါတယ်
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Username'})
    self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your Password'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your Password'})