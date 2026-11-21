import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import FileResponse, Http404
from django.views.decorators.http import require_http_methods

from .models import EvidenceFile
from .forms import EvidenceUploadForm
from cases.models import CaseRecord
from accounts.decorators import field_officer_required
from auditlog.utils import log_audit


@login_required
@field_officer_required
@require_http_methods(["GET", "POST"])
def evidence_upload_view(request, case_id):
    """Secure evidence upload view with server-side extension, MIME, and size validation."""
    case = get_object_or_404(CaseRecord, pk=case_id)
    if not case.can_user_edit(request.user):
        messages.error(request, f"Cannot upload evidence: Case {case.case_reference} is locked in '{case.status}' status.")
        raise PermissionDenied("Case is locked for evidence modifications.")

    if request.method == 'POST':
        form = EvidenceUploadForm(request.POST, request.FILES, case=case)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.case = case
            evidence.uploaded_by = request.user
            file_obj = request.FILES['file']
            evidence.original_filename = file_obj.name
            evidence.file_size = file_obj.size
            evidence.content_type = getattr(file_obj, 'content_type', 'application/octet-stream')
            evidence.save()

            log_audit(
                request,
                'EVIDENCE_UPLOAD',
                evidence,
                f"Uploaded evidence attachment '{evidence.original_filename}' ({evidence.file_size_display}) for case {case.case_reference}."
            )
            messages.success(request, f"Evidence file '{evidence.original_filename}' uploaded securely.")
            return redirect('case_detail', pk=case.pk)
    else:
        form = EvidenceUploadForm(case=case)

    return render(request, 'evidence/evidence_upload_form.html', {
        'form': form,
        'case': case,
        'title': f"Upload Evidence for {case.case_reference}",
    })


@login_required
def evidence_download_view(request, pk):
    """
    Authorized private evidence file access endpoint.
    Verifies user authentication and permissions. Never serves raw file paths publicly.
    """
    evidence = get_object_or_404(EvidenceFile.objects.select_related('case'), pk=pk)

    if not evidence.file or not os.path.exists(evidence.file.path):
        raise Http404("The requested evidentiary file is unavailable on secure storage.")

    response = FileResponse(open(evidence.file.path, 'rb'), content_type=evidence.content_type)
    # Inline viewing for PDF and images, download for others
    if evidence.is_image or evidence.is_pdf:
        response['Content-Disposition'] = f'inline; filename="{evidence.original_filename}"'
    else:
        response['Content-Disposition'] = f'attachment; filename="{evidence.original_filename}"'
    return response
