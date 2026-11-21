from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import TestEvent, TestKit, PRESUMPTIVE_DISCLAIMER
from .forms import TestEventForm, TestKitForm
from cases.models import Sample
from accounts.decorators import role_required, field_officer_required, supervisor_required, admin_required
from auditlog.utils import log_audit


@login_required
@field_officer_required
@require_http_methods(["GET", "POST"])
def test_event_create_view(request, sample_id):
    """
    Documents a field presumptive screening test event for a specific sample.
    Enforces persistent presumptive disclaimer and kit validation.
    """
    sample = get_object_or_404(Sample.objects.select_related('case'), pk=sample_id)
    case = sample.case

    if not case.can_user_edit(request.user):
        messages.error(request, f"Cannot record test event: Case {case.case_reference} is in '{case.status}' status and locked.")
        raise PermissionDenied("Case is locked for documentation additions.")

    if request.method == 'POST':
        form = TestEventForm(request.POST)
        if form.is_valid():
            test_event = form.save(commit=False)
            test_event.sample = sample
            test_event.performed_by = request.user
            test_event.save()

            log_audit(
                request,
                'TEST_RECORDED',
                test_event,
                f"Recorded {test_event.result_category} for {sample.sample_code} using {test_event.kit.name}."
            )
            messages.success(request, f"Presumptive test event recorded successfully for {sample.sample_code}.")
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = TestEventForm()

    return render(request, 'testing_records/test_event_form.html', {
        'form': form,
        'sample': sample,
        'case': case,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
        'title': f"Record Presumptive Test for {sample.sample_code}",
    })


@login_required
def kit_list_view(request):
    """Lists approved test kit catalogue entries."""
    kits = TestKit.objects.all().order_by('name')
    return render(request, 'testing_records/kit_list.html', {
        'kits': kits,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


@login_required
@role_required('Supervisor', 'Administrator')
@require_http_methods(["GET", "POST"])
def kit_create_view(request):
    """Adds a new test kit catalogue entry."""
    if request.method == 'POST':
        form = TestKitForm(request.POST)
        if form.is_valid():
            kit = form.save()
            log_audit(
                request,
                'CREATE',
                kit,
                f"Added test kit catalogue entry: {kit.name} ({kit.catalogue_reference})."
            )
            messages.success(request, f"Test kit '{kit.name}' added to catalogue.")
            return redirect('kit_list')
    else:
        form = TestKitForm()

    return render(request, 'testing_records/kit_form.html', {
        'form': form,
        'title': 'Add Test Kit to Catalogue',
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


@login_required
@role_required('Supervisor', 'Administrator')
@require_http_methods(["GET", "POST"])
def kit_edit_view(request, pk):
    """Edits test kit catalogue metadata."""
    kit = get_object_or_404(TestKit, pk=pk)
    if request.method == 'POST':
        form = TestKitForm(request.POST, instance=kit)
        if form.is_valid():
            kit = form.save()
            log_audit(
                request,
                'UPDATE',
                kit,
                f"Updated test kit metadata: {kit.name} ({kit.catalogue_reference})."
            )
            messages.success(request, f"Test kit '{kit.name}' updated.")
            return redirect('kit_list')
    else:
        form = TestKitForm(instance=kit)

    return render(request, 'testing_records/kit_form.html', {
        'form': form,
        'kit': kit,
        'title': f"Edit Test Kit: {kit.name}",
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })
