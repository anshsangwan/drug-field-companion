from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cases.models import CaseRecord, Sample
from testing_records.models import PRESUMPTIVE_DISCLAIMER
from auditlog.models import AuditEvent


def landing_view(request):
    """Public landing page; redirects authenticated users directly to their dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html', {
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


@login_required
def dashboard_view(request):
    """
    Role-aware operational dashboard providing key forensic performance indicators,
    pending supervisory tasks, recent activity feed, and contextual shortcuts.
    """
    user = request.user
    total_cases = CaseRecord.objects.count()
    active_cases = CaseRecord.objects.filter(
        status__in=[CaseRecord.STATUS_DRAFT, CaseRecord.STATUS_SUBMITTED, CaseRecord.STATUS_CHANGES_REQUESTED]
    ).count()
    total_samples = Sample.objects.count()
    pending_reviews = CaseRecord.objects.filter(status=CaseRecord.STATUS_SUBMITTED).count()
    approved_cases = CaseRecord.objects.filter(status=CaseRecord.STATUS_APPROVED).count()

    recent_cases = CaseRecord.objects.select_related('created_by', 'assigned_to').order_by('-created_at')[:5]
    pending_review_list = CaseRecord.objects.filter(
        status=CaseRecord.STATUS_SUBMITTED
    ).select_related('created_by').order_by('updated_at')[:5]
    recent_activities = AuditEvent.objects.select_related('actor').order_by('-timestamp')[:8]

    return render(request, 'core/dashboard.html', {
        'total_cases': total_cases,
        'active_cases': active_cases,
        'total_samples': total_samples,
        'pending_reviews': pending_reviews,
        'approved_cases': approved_cases,
        'recent_cases': recent_cases,
        'pending_review_list': pending_review_list,
        'recent_activities': recent_activities,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


def custom_permission_denied_view(request, exception=None):
    return render(request, 'core/403.html', status=403)


def custom_page_not_found_view(request, exception=None):
    return render(request, 'core/404.html', status=404)


def custom_server_error_view(request):
    return render(request, 'core/500.html', status=500)
