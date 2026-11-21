# Accounts context processors
def user_roles(request):
    if not request.user.is_authenticated:
        return {
            'is_field_officer': False,
            'is_supervisor': False,
            'is_admin_user': False,
            'is_readonly_user': False,
            'user_role_label': 'Guest',
        }
    groups = set(request.user.groups.values_list('name', flat=True))
    is_admin = request.user.is_superuser or 'Administrator' in groups
    is_supervisor = 'Supervisor' in groups or is_admin
    is_field_officer = 'Field Officer' in groups or is_admin
    is_readonly = 'Read-only User' in groups and not (is_admin or is_supervisor or is_field_officer)

    role_label = 'Administrator' if is_admin else ('Supervisor' if is_supervisor else ('Field Officer' if is_field_officer else ('Read-only User' if is_readonly else 'User')))

    return {
        'is_field_officer': is_field_officer,
        'is_supervisor': is_supervisor,
        'is_admin_user': is_admin,
        'is_readonly_user': is_readonly,
        'user_role_label': role_label,
    }
