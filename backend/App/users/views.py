# the project is session based to stop CRSF+XSS
# defined endpoints 



from django.contrib import messages
from django.shortcuts import render,redirect
import json 
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

# Create your views here.

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.shortcuts import (
    redirect,
    render,
)
from django.contrib.auth.decorators import login_required

from .forms import (
    CustomLoginForm,
    RegisterForm,
    ForgetPasswordEmailCodeForm,
    ChangePasswordForm,
    OtpForm,
    ProfileUpdateForm,
    UserUpdateForm,
    
)
from .models import OtpCode, user,Notification
from .utils import (
    send_activation_code,
    send_reset_password_code,
)
from .decorators import only_authenticated_user, redirect_authenticated_user

@only_authenticated_user
def home_view(request):
    return render(request, 'users/home.html')


@redirect_authenticated_user
def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username_or_email'], password=form.cleaned_data['password'])
            if user:
                if not user.is_active:
                    messages.warning(request, _(
                        f"It's look like you haven't still verify your email - {user.email}"))
                    return redirect('users:activate_email')
                else:
                    login(request, user)
                    return redirect('users:login')
            else:
                error = 'Invalid Credentials'
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})


@only_authenticated_user
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@redirect_authenticated_user
def registeration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.source = 'Register'
            user.save(True)

            code = get_random_string(10)
            otp = OtpCode(code=code, user=user)
            otp.save(True)
            try:
                send_activation_code(user.email, code)
            except:
                otp.delete()
                user.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(
                    request, _(f'We have sent a verification code to your email - {user.email}'))
                return redirect('users:activate_email')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})



def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordEmailCodeForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user = get_user_model().objects.get(**username_or_email)
            code = get_random_string(20)

            otp = OtpCode(code=code, user=user, email=user.email)
            otp.save()

            try:
                send_reset_password_code(user.email, code)
            except:
                otp.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(request, _(
                    f"We've sent a passwrod reset otp to your email - {user.email}"))
                return redirect('users:reset_code')
    else:
        form = ForgetPasswordEmailCodeForm()
    return render(request, 'users/forgot_password.html', context={'form': form})


def check_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            user = otp.user
            otp.delete()
            user.is_active = True
            user.save()
            return redirect('users:home')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})


def check_reset_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            request.session['email'] = otp.user.email
            messages.success(request, _(
                "Please create a new password that you don't use on any other site."))
            return redirect('users:reset_new_password')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})



def reset_new_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            email = request.session['email']
            del request.session['email']
            user_instance = get_user_model().objects.get(email=email)  # Use a different variable name
            user_instance.password = make_password(form.cleaned_data["new_password2"])
            user_instance.save()
            messages.success(request, _(
                "Your password has been changed. Now you can login with your new password."))
            return redirect('users:login')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/new_password.html', {'form': form})

@login_required
def delete_account_view(request):
    # Delete the user account
    request.user.delete()
    # Redirect to home page or any other page
    return redirect('users:login')


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_update.html', context)





def new_message(request):
    # Logic to send message...
    recipient = request.user  # Assuming the recipient is the current user
    message = "You have a new message!"
    Notification.objects.create(recipient=recipient, message=message)

# Displaying notifications
def view_notifications(request):
    # Retrieve and mark all unread notifications for the current user as read
    user_notifications = Notification.objects.filter(recipient=request.user)
    user_notifications.update(is_read=True)
    
    # Retrieve the total count of unread notifications for display
    total_unread_notifications = user_notifications.count()
    
    # Render the notifications page with the updated notifications
    return render(request, 'users/notifications.html', {'notifications': user_notifications, 'total_unread_notifications': total_unread_notifications})