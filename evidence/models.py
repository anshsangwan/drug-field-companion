from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
import os


def validate_file_extension_and_size(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_exts = getattr(settings, 'ALLOWED_EVIDENCE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.pdf'])
    if ext not in allowed_exts:
        raise ValidationError(
            f"Unsupported file format '{ext}'. Only permitted attachments are: {', '.join(allowed_exts)}"
        )
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if value.size > max_size:
        size_mb = max_size / (1024 * 1024)
        raise ValidationError(f"File size exceeds maximum allowed limit of {size_mb:.0f} MB.")


class EvidenceFile(models.Model):
    """
    Evidence attachment record stored in a private vault directory.
    Access is strictly controlled via authenticated and authorized views.
    """
    case = models.ForeignKey(
        'cases.CaseRecord',
        on_delete=models.CASCADE,
        related_name='evidence_files'
    )
    sample = models.ForeignKey(
        'cases.Sample',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_files',
        help_text="Optional association with a specific specimen."
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='uploaded_evidence'
    )
    file = models.FileField(
        upload_to='evidence_vault/%Y/%m/',
        validators=[validate_file_extension_and_size]
    )
    original_filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    file_size = models.IntegerField(help_text="File size in bytes.")
    caption = models.CharField(
        max_length=255,
        help_text="Descriptive caption or photo documentation note."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Evidence File'
        verbose_name_plural = 'Evidence Files'

    def __str__(self):
        return f"{self.original_filename} ({self.case.case_reference})"

    @property
    def file_size_display(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size / (1024 * 1024):.1f} MB"

    @property
    def is_image(self):
        return self.content_type.startswith('image/') or self.original_filename.lower().endswith(('.jpg', '.jpeg', '.png'))

    @property
    def is_pdf(self):
        return self.content_type == 'application/pdf' or self.original_filename.lower().endswith('.pdf')
