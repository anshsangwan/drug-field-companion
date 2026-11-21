from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q
from django.utils import timezone

from .models import CaseRecord, Sample
from .forms import CaseRecordForm, SampleForm
from accounts.decorators import role_required, field_officer_required
from auditlog.utils import log_audit
from testing_records.models import PRESUMPTIVE_DISCLAIMER
from custody.models import CustodyEvent


@login_required
def case_list_view(request):
    """
    Searchable, filterable, and paginated list of cases.
    Enforces role-aware record viewing policies.
    """
    qs = CaseRecord.objects.select_related('created_by', 'assigned_to').all()

    # Query search
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(case_reference__icontains=q) |
            Q(title__icontains=q) |
            Q(general_location__icontains=q) |
            Q(description__icontains=q)
        )

    # Status filter
    status = request.GET.get('status', '').strip()
    if status:
        qs = qs.filter(status=status)

    # Date filters
    date_from = request.GET.get('date_from', '').strip()
    if date_from:
        try:
            qs = qs.filter(incident_datetime__date__gte=date_from)
        except Exception:
            pass

    date_to = request.GET.get('date_to', '').strip()
    if date_to:
        try:
            qs = qs.filter(incident_datetime__date__lte=date_to)
        except Exception:
            pass

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cases/case_list.html', {
        'page_obj': page_obj,
        'q': q,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': CaseRecord.STATUS_CHOICES,
    })


@login_required
def case_detail_view(request, pk):
    """
    Comprehensive case dashboard presenting metadata, related samples,
    test records, chain-of-custody overview, evidence files, and supervisory reviews.
    """
    case = get_object_or_404(
        CaseRecord.objects.select_related('created_by', 'assigned_to'),
        pk=pk
    )

    samples = case.samples.all().prefetch_related(
        'test_events__kit',
        'test_events__performed_by',
        'custody_events__recorded_by'
    )
    evidence_files = case.evidence_files.select_related('uploaded_by', 'sample').all()
    review_records = case.review_records.select_related('reviewer').all()

    can_edit = case.can_user_edit(request.user)
    can_submit = case.can_user_submit(request.user)

    return render(request, 'cases/case_detail.html', {
        'case': case,
        'samples': samples,
        'evidence_files': evidence_files,
        'review_records': review_records,
        'can_edit': can_edit,
        'can_submit': can_submit,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


@login_required
@field_officer_required
@require_http_methods(["GET", "POST"])
def case_create_view(request):
    """Creates a new CaseRecord in Draft status."""
    if request.method == 'POST':
        form = CaseRecordForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user
            case.status = CaseRecord.STATUS_DRAFT
            case.save()
            log_audit(
                request,
                'CREATE',
                case,
                f"Created case {case.case_reference} ({case.title}) in Draft status."
            )
            messages.success(request, f"Case {case.case_reference} created successfully.")
            return redirect('case_detail', pk=case.pk)
    else:
        form = CaseRecordForm()

    return render(request, 'cases/case_form.html', {
        'form': form,
        'title': 'Create New Case Record',
    })


@login_required
@require_http_methods(["GET", "POST"])
def case_edit_view(request, pk):
    """Updates an existing CaseRecord when permitted by workflow status and role."""
    case = get_object_or_404(CaseRecord, pk=pk)
    if not case.can_user_edit(request.user):
        messages.error(request, f"Case {case.case_reference} cannot be edited in '{case.status}' status or by your role.")
        raise PermissionDenied("You do not have permission to edit this case.")

    if request.method == 'POST':
        form = CaseRecordForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save()
            log_audit(
                request,
                'UPDATE',
                case,
                f"Updated details for case {case.case_reference}."
            )
            messages.success(request, f"Case {case.case_reference} updated successfully.")
            return redirect('case_detail', pk=case.pk)
    else:
        form = CaseRecordForm(instance=case)

    return render(request, 'cases/case_form.html', {
        'form': form,
        'case': case,
        'title': f"Edit Case: {case.case_reference}",
    })


@login_required
@require_POST
def case_submit_view(request, pk):
    """Submits a case for supervisory verification."""
    case = get_object_or_404(CaseRecord, pk=pk)
    if not case.can_user_submit(request.user):
        messages.error(request, f"Case {case.case_reference} cannot be submitted from '{case.status}' status.")
        return redirect('case_detail', pk=case.pk)

    if not case.samples.exists():
        messages.error(request, "Cannot submit case for review without at least one registered sample.")
        return redirect('case_detail', pk=case.pk)

    case.status = CaseRecord.STATUS_SUBMITTED
    case.save(update_fields=['status', 'updated_at'])

    log_audit(
        request,
        'SUBMIT',
        case,
        f"Case {case.case_reference} submitted for supervisory review by {request.user.username}."
    )
    messages.success(request, f"Case {case.case_reference} has been submitted for supervisory review.")
    return redirect('case_detail', pk=case.pk)


@login_required
@field_officer_required
@require_http_methods(["GET", "POST"])
def sample_create_view(request, case_id):
    """Registers a new sample associated with a Case."""
    case = get_object_or_404(CaseRecord, pk=case_id)
    if not case.can_user_edit(request.user):
        messages.error(request, f"Cannot add samples: Case is currently in '{case.status}' status.")
        raise PermissionDenied("Case is locked for editing.")

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.case = case
            sample.created_by = request.user
            sample.save()

            # Record initial collection custody event automatically
            CustodyEvent.objects.create(
                sample=sample,
                event_type=CustodyEvent.TYPE_COLLECTION,
                event_at=sample.collected_at,
                from_person=f"Field Collection / Scene ({case.general_location})",
                to_person=request.user.get_full_name() or request.user.username,
                location_reference=f"Secured at {case.general_location}",
                seal_reference=sample.seal_reference,
                remarks=f"Initial field collection. Condition: {sample.initial_condition}.",
                recorded_by=request.user
            )

            log_audit(
                request,
                'CREATE',
                sample,
                f"Registered sample {sample.sample_code} under case {case.case_reference}."
            )
            messages.success(request, f"Sample {sample.sample_code} registered successfully.")
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = SampleForm()

    return render(request, 'cases/sample_form.html', {
        'form': form,
        'case': case,
        'title': f"Register Sample for {case.case_reference}",
    })


@login_required
def sample_detail_view(request, pk):
    """Detailed view for a single physical specimen."""
    sample = get_object_or_404(
        Sample.objects.select_related('case', 'created_by'),
        pk=pk
    )
    test_events = sample.test_events.select_related('kit', 'performed_by').all()
    custody_events = sample.custody_events.select_related('recorded_by').all()
    evidence_files = sample.evidence_files.select_related('uploaded_by').all()
    can_edit = sample.case.can_user_edit(request.user)

    return render(request, 'cases/sample_detail.html', {
        'sample': sample,
        'case': sample.case,
        'test_events': test_events,
        'custody_events': custody_events,
        'evidence_files': evidence_files,
        'can_edit': can_edit,
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })


@login_required
@require_http_methods(["GET", "POST"])
def sample_edit_view(request, pk):
    """Edits sample description or metadata if case is editable."""
    sample = get_object_or_404(Sample.objects.select_related('case'), pk=pk)
    if not sample.case.can_user_edit(request.user):
        messages.error(request, "Cannot edit sample: Case is locked.")
        raise PermissionDenied("Case is locked for editing.")

    if request.method == 'POST':
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            sample = form.save()
            log_audit(
                request,
                'UPDATE',
                sample,
                f"Updated sample metadata for {sample.sample_code}."
            )
            messages.success(request, f"Sample {sample.sample_code} updated successfully.")
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = SampleForm(instance=sample)

    return render(request, 'cases/sample_form.html', {
        'form': form,
        'case': sample.case,
        'sample': sample,
        'title': f"Edit Sample {sample.sample_code}",
    })


@login_required
def case_report_view(request, pk):
    """
    Print-friendly, official documentation summary report for a Case.
    Suitable for browser print / Save to PDF.
    """
    case = get_object_or_404(
        CaseRecord.objects.select_related('created_by', 'assigned_to'),
        pk=pk
    )
    samples = case.samples.all().prefetch_related(
        'test_events__kit',
        'test_events__performed_by',
        'custody_events__recorded_by'
    )
    evidence_files = case.evidence_files.select_related('uploaded_by', 'sample').all()
    review_records = case.review_records.select_related('reviewer').all()

    return render(request, 'cases/case_report.html', {
        'case': case,
        'samples': samples,
        'evidence_files': evidence_files,
        'review_records': review_records,
        'report_generated_at': timezone.now(),
        'presumptive_disclaimer': PRESUMPTIVE_DISCLAIMER,
    })
