from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class CaseRecord(models.Model):
    """
    Parent forensic case record representing an incident or field operation.
    Enforces status workflow: Draft -> Submitted -> Changes requested -> Approved -> Archived.
    """
    STATUS_DRAFT = 'Draft'
    STATUS_SUBMITTED = 'Submitted'
    STATUS_CHANGES_REQUESTED = 'Changes requested'
    STATUS_APPROVED = 'Approved'
    STATUS_ARCHIVED = 'Archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft (Work in Progress)'),
        (STATUS_SUBMITTED, 'Submitted (Awaiting Supervisory Review)'),
        (STATUS_CHANGES_REQUESTED, 'Changes Requested (Returned for Correction)'),
        (STATUS_APPROVED, 'Approved (Verified by Supervisor)'),
        (STATUS_ARCHIVED, 'Archived (Retention State)'),
    ]

    case_reference = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="Unique auto-generated case reference identifier (e.g. CASE-2026-0001)."
    )
    title = models.CharField(max_length=255, help_text="Short operational title or incident summary.")
    incident_datetime = models.DateTimeField(
        help_text="Date and time when the field incident occurred or was initiated."
    )
    general_location = models.CharField(
        max_length=255,
        help_text="General field location (e.g., Highway 101 Mile 42, Port Terminal B)."
    )
    description = models.TextField(
        help_text="Detailed context and operational background for the field test assignment."
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_cases'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Case Record'
        verbose_name_plural = 'Case Records'

    def __str__(self):
        return f"{self.case_reference} - {self.title}"

    @classmethod
    def generate_unique_reference(cls):
        year = timezone.now().year
        # Find next sequential ID for this year
        prefix = f"CASE-{year}-"
        cases_this_year = cls.objects.filter(case_reference__startswith=prefix).count()
        candidate = f"{prefix}{cases_this_year + 1:04d}"
        # Ensure collision safety
        while cls.objects.filter(case_reference=candidate).exists():
            cases_this_year += 1
            candidate = f"{prefix}{cases_this_year + 1:04d}"
        return candidate

    def save(self, *args, **kwargs):
        if not self.case_reference:
            self.case_reference = self.generate_unique_reference()
        super().save(*args, **kwargs)

    @property
    def is_editable(self):
        """Case is editable during initial draft or when supervisor requested corrections."""
        return self.status in [self.STATUS_DRAFT, self.STATUS_CHANGES_REQUESTED]

    def can_user_edit(self, user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        user_groups = set(user.groups.values_list('name', flat=True))
        if 'Administrator' in user_groups or 'Supervisor' in user_groups:
            return True
        if 'Field Officer' in user_groups and self.created_by == user:
            return self.is_editable
        return False

    def can_user_submit(self, user):
        if not user.is_authenticated:
            return False
        if not self.is_editable:
            return False
        if user.is_superuser:
            return True
        user_groups = set(user.groups.values_list('name', flat=True))
        return ('Field Officer' in user_groups and self.created_by == user) or 'Supervisor' in user_groups


class Sample(models.Model):
    """
    A uniquely identified physical item or evidentiary specimen associated with a Case.
    """
    sample_code = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="Unique sample code (e.g., SMP-2026-0001)."
    )
    case = models.ForeignKey(
        CaseRecord,
        on_delete=models.CASCADE,
        related_name='samples'
    )
    collected_at = models.DateTimeField(
        help_text="Date and time when the sample was formally secured/collected."
    )
    description = models.TextField(
        help_text="Physical description of specimen (e.g. White powdery substance inside plastic baggie)."
    )
    packaging_reference = models.CharField(
        max_length=128,
        help_text="Primary packaging description (e.g. Tamper-evident evidence pouch #4812)."
    )
    seal_reference = models.CharField(
        max_length=128,
        help_text="Numbered integrity seal reference (e.g. RED-SEAL-8831)."
    )
    initial_condition = models.CharField(
        max_length=255,
        help_text="Condition upon collection (e.g., Intact, Dry, Sealed)."
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_samples'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Sample'
        verbose_name_plural = 'Samples'

    def __str__(self):
        return f"{self.sample_code} ({self.case.case_reference})"

    @classmethod
    def generate_unique_code(cls):
        year = timezone.now().year
        prefix = f"SMP-{year}-"
        count = cls.objects.filter(sample_code__startswith=prefix).count()
        candidate = f"{prefix}{count + 1:04d}"
        while cls.objects.filter(sample_code=candidate).exists():
            count += 1
            candidate = f"{prefix}{count + 1:04d}"
        return candidate

    def save(self, *args, **kwargs):
        if not self.sample_code:
            self.sample_code = self.generate_unique_code()
        super().save(*args, **kwargs)
