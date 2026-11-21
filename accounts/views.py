from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from .forms import LoginForm, UserCreateForm, UserUpdateForm
from .decorators import admin_required
from auditlog.utils import log_audit


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            log_audit(request, 'LOGIN', user, f"User {user.username} logged in successfully.")
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}.")
            next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm(request)

    return render(request, 'registration/login.html', {'form': form})


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        log_audit(request, 'LOGOUT', request.user, f"User {username} logged out.")
        logout(request)
        messages.info(request, "You have been securely logged out.")
    return redirect('login')


@login_required
@admin_required
def user_list_view(request):
    users = User.objects.all().prefetch_related('groups').order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def user_create_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_audit(
                request,
                'USER_MANAGEMENT',
                user,
                f"Created new user account '{user.username}' with role '{form.cleaned_data['role']}'."
            )
            messages.success(request, f"User '{user.username}' created successfully.")
            return redirect('user_list')
    else:
        form = UserCreateForm()

    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create New User Account'})


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def user_edit_view(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            log_audit(
                request,
                'USER_MANAGEMENT',
                user_obj,
                f"Updated user account '{user_obj.username}' (role: {form.cleaned_data['role']}, active: {user_obj.is_active})."
            )
            messages.success(request, f"User '{user_obj.username}' updated successfully.")
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user_obj)

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'user_obj': user_obj,
        'title': f"Edit User: {user_obj.username}"
    })


@login_required
@admin_required
@require_POST
def user_toggle_active_view(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if user_obj == request.user:
        messages.error(request, "You cannot deactivate your own administrative account.")
        return redirect('user_list')

    user_obj.is_active = not user_obj.is_active
    user_obj.save(update_fields=['is_active'])
    status_str = "activated" if user_obj.is_active else "deactivated"
    log_audit(request, 'USER_MANAGEMENT', user_obj, f"Account '{user_obj.username}' was {status_str}.")
    messages.success(request, f"User account '{user_obj.username}' has been {status_str}.")
    return redirect('user_list')
