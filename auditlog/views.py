from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import AuditEvent
from accounts.decorators import role_required


@login_required
@role_required('Administrator', 'Supervisor', 'Read-only User')
def audit_list_view(request):
    """
    Searchable audit trail display.
    Accessible to administrators, supervisors, and compliance/auditor roles.
    """
    qs = AuditEvent.objects.select_related('actor').all()

    action = request.GET.get('action', '').strip()
    if action:
        qs = qs.filter(action=action)

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(summary__icontains=q) |
            Q(object_type__icontains=q) |
            Q(object_id__icontains=q) |
            Q(actor__username__icontains=q)
        )

    paginator = Paginator(qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'auditlog/audit_list.html', {
        'page_obj': page_obj,
        'selected_action': action,
        'q': q,
        'action_choices': AuditEvent.ACTION_CHOICES,
    })
