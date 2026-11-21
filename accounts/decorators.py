from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def is_in_group(user, group_name):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()


def is_field_officer(user):
    return is_in_group(user, 'Field Officer') or user.is_superuser


def is_supervisor(user):
    return is_in_group(user, 'Supervisor') or user.is_superuser


def is_admin_user(user):
    return is_in_group(user, 'Administrator') or user.is_superuser


def is_readonly_user(user):
    if not user.is_authenticated:
        return False
    return is_in_group(user, 'Read-only User') and not (is_admin_user(user) or is_supervisor(user) or is_field_officer(user))


def role_required(*allowed_roles):
    """
    Decorator requiring user to belong to at least one of the specified roles or be superuser.
    Roles can be: 'Field Officer', 'Supervisor', 'Administrator', 'Read-only User'
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = set(request.user.groups.values_list('name', flat=True))
            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            messages.error(request, "Access denied. You do not possess the required role permission.")
            raise PermissionDenied("You do not have permission to access this resource.")
        return _wrapped_view
    return decorator


def field_officer_required(view_func):
    return role_required('Field Officer', 'Supervisor', 'Administrator')(view_func)


def supervisor_required(view_func):
    return role_required('Supervisor', 'Administrator')(view_func)


def admin_required(view_func):
    return role_required('Administrator')(view_func)
