from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction

from .models import ReviewRecord
from .forms import ReviewForm
from cases.models import CaseRecord
from accounts.decorators import supervisor_required
from auditlog.utils import log_audit
from testing_records.models import PRESUMPTIVE_DISCLAIMER


@login_required
@supervisor_required
@require_http_methods(["GET", "POST"])
def review_create_view(request, case_id):
    """
    Supervisory review view.
    Authorizes supervisors to approve case documentation or return it with mandatory correction instructions.
    """
    case = get_object_or_404(
        CaseRecord.objects.select_related('created_by'),
        pk=case_id
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.case = case
                review.reviewer = request.user
                review.save()

                if review.decision == ReviewRecord.DECISION_APPROVED:
                    case.status = CaseRecord.STATUS_APPROVED
                    action_type = 'REVIEW_APPROVED'
                    msg = f"Documentation for case {case.case_reference} has been formally approved."
                else:
                    case.status = CaseRecord.STATUS_CHANGES_REQUESTED
                    action_type = 'REVIEW_CHANGES_REQUESTED'
                    msg = f"Case {case.case_reference} returned to field officer with requested revisions."

                case.save(update_fields=['status', 'updated_at'])

                log_audit(
                    request,
                    action_type,
                    review,
                    f"Supervisor {request.user.username} {review.decision.lower()} case {case.case_reference}. Comments: {review.comment}"
                )

            messages.success(request, msg)
            return redirect('case_detail', pk=case.pk)
    else:
        form = ReviewForm()

    samples = case.samples.all().prefetch_related(
        'test_events__kit',
        'custody_events__recorded_by'
    )
    evidence_files = case.evidence_files.all()
    review_history = case.review_records.select_related('reviewer').all()

    return render(request, 'reviews/review_form.html', {
        'case': case,
        'form': form,
        'samples': samples,
        'evidence_files': evidence_files,
        'review_history': review_history,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
        'title': f"Supervisor Review: {case.case_reference}",
    })


@login_required
@supervisor_required
def review_list_view(request):
    """Dashboard queue of cases awaiting supervisory verification."""
    pending_cases = CaseRecord.objects.filter(
        status=CaseRecord.STATUS_SUBMITTED
    ).select_related('created_by', 'assigned_to').order_by('updated_at')

    recent_reviews = ReviewRecord.objects.select_related(
        'case', 'reviewer'
    ).order_by('-reviewed_at')[:15]

    return render(request, 'reviews/review_list.html', {
        'pending_cases': pending_cases,
        'recent_reviews': recent_reviews,
    })
