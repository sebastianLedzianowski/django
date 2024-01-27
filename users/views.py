from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str

from .forms import RegisterForm, LoginForm, ProfileForm, CustomPasswordResetForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, authenticate

from django.core.mail import send_mail

def send_reset_email(user, reset_url):
    subject = 'Password Reset'
    message = f'Click the link below to reset your password:\n\n{reset_url}'
    from_email = 'password.reset@localhost.com'
    recipient_list = [user.email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except User.DoesNotExist:
                messages.error(request, 'The email does not exist in the database. Please try again.')
                user = None

            if user:
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_str(user.pk).encode())
                reset_url = f"{request.scheme}://{request.get_host()}/reset/{uidb64}/{token}/"

                send_reset_email(user, reset_url)

                messages.success(request, 'Password reset email has been sent.')
                return redirect('users:login')

    else:
        form = CustomPasswordResetForm()

    return render(request, 'users/custom_password_reset.html', {'form': form})


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=user.username, password=request.POST['new_password1'])
                login(request, user)
                messages.success(request, 'Your password has been successfully reset.')
                return redirect('home')
        else:
            form = SetPasswordForm(user)

        return render(request, 'users/custom_password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset')

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='home')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='home')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})
