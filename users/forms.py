from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    email = forms.EmailField(max_length=200,
                             required=True,
                             help_text='Required. Please enter a valid email address.',
                             widget=forms.EmailInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
