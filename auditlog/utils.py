from .models import AuditEvent


def get_client_ip(request):
    """Safely extracts client IP address from HttpRequest."""
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_audit(actor_or_request, action, obj, summary):
    """
    Convenience utility to record an AuditEvent.
    actor_or_request can be an HttpRequest or a User instance (or None).
    """
    actor = None
    ip = None

    # Check if request passed
    if hasattr(actor_or_request, 'user'):
        actor = actor_or_request.user if actor_or_request.user.is_authenticated else None
        ip = get_client_ip(actor_or_request)
    else:
        actor = actor_or_request

    obj_type = obj.__class__.__name__ if hasattr(obj, '__class__') else str(type(obj))
    obj_id = str(getattr(obj, 'pk', getattr(obj, 'id', 'N/A')))

    return AuditEvent.objects.create(
        actor=actor,
        action=action,
        object_type=obj_type,
        object_id=obj_id,
        summary=summary,
        ip_address=ip
    )
