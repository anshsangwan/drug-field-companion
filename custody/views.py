from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import CustodyEvent
from .forms import CustodyEventForm
from cases.models import Sample
from accounts.decorators import field_officer_required
from auditlog.utils import log_audit


@login_required
@field_officer_required
@require_http_methods(["GET", "POST"])
def custody_event_create_view(request, sample_id):
    """
    Records an append-only chain of custody entry.
    Flags unusual chronology if recorded event timestamp precedes existing entries.
    """
    sample = get_object_or_404(Sample.objects.select_related('case'), pk=sample_id)
    case = sample.case

    if request.method == 'POST':
        form = CustodyEventForm(request.POST)
        if form.is_valid():
            custody_event = form.save(commit=False)
            custody_event.sample = sample
            custody_event.recorded_by = request.user
            custody_event.save()

            if custody_event.is_out_of_sequence:
                messages.warning(
                    request,
                    f"Notice: Custody event timestamp ({custody_event.event_at:%Y-%m-%d %H:%M}) is earlier than existing records for this specimen. Marked as out-of-sequence entry for auditability."
                )

            log_audit(
                request,
                'CUSTODY_RECORDED',
                custody_event,
                f"Custody event [{custody_event.event_type}] logged for {sample.sample_code}: {custody_event.from_person} -> {custody_event.to_person}."
            )
            messages.success(request, f"Chain-of-custody transfer successfully recorded for {sample.sample_code}.")
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = CustodyEventForm()

    return render(request, 'custody/custody_event_form.html', {
        'form': form,
        'sample': sample,
        'case': case,
        'title': f"Log Custody Transfer for {sample.sample_code}",
    })


@login_required
def custody_timeline_view(request, sample_id):
    """Timeline view of all custody transactions for a specific sample."""
    sample = get_object_or_404(Sample.objects.select_related('case'), pk=sample_id)
    events = sample.custody_events.select_related('recorded_by').order_by('event_at', 'created_at')
    return render(request, 'custody/custody_timeline.html', {
        'sample': sample,
        'case': sample.case,
        'events': events,
    })
