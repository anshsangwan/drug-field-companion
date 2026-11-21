from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustodyEvent(models.Model):
    """
    Chronological Chain of Custody entry.
    Append-only tracking of physical item possession, transfers, storage, and integrity checks.
    Never silently modified or deleted in ordinary operation.
    """
    TYPE_COLLECTION = 'Collection'
    TYPE_TRANSFER = 'Transfer'
    TYPE_RECEIVED = 'Received'
    TYPE_STORED = 'Stored'
    TYPE_STORAGE_CHANGED = 'Storage location changed'
    TYPE_RELEASED = 'Released'
    TYPE_RETURNED = 'Returned'
    TYPE_SEALED = 'Sealed/Resealed'
    TYPE_OTHER = 'Other'

    EVENT_TYPE_CHOICES = [
        (TYPE_COLLECTION, 'Collection (Initial Securement)'),
        (TYPE_TRANSFER, 'Transfer (Handover)'),
        (TYPE_RECEIVED, 'Received (Custody Accepted)'),
        (TYPE_STORED, 'Stored (Placed in Evidence Locker/Vault)'),
        (TYPE_STORAGE_CHANGED, 'Storage Location Changed'),
        (TYPE_RELEASED, 'Released (To Lab/Court/Disposal)'),
        (TYPE_RETURNED, 'Returned (To Vault/Owner)'),
        (TYPE_SEALED, 'Sealed/Resealed (Integrity Check)'),
        (TYPE_OTHER, 'Other'),
    ]

    sample = models.ForeignKey(
        'cases.Sample',
        on_delete=models.CASCADE,
        related_name='custody_events'
    )
    event_type = models.CharField(max_length=64, choices=EVENT_TYPE_CHOICES)
    event_at = models.DateTimeField(help_text="Exact date and time when the physical custody event took place.")
    from_person = models.CharField(max_length=128, help_text="Name, badge number, or official role of releasing party.")
    to_person = models.CharField(max_length=128, help_text="Name, badge number, or official role of receiving party.")
    location_reference = models.CharField(
        max_length=255,
        help_text="Secure storage facility, locker number, or transit location."
    )
    seal_reference = models.CharField(
        max_length=128,
        blank=True,
        default="",
        help_text="Verification of intact seal number at time of event."
    )
    remarks = models.TextField(blank=True, default="", help_text="Contextual details or transfer reasons.")
    is_out_of_sequence = models.BooleanField(
        default=False,
        help_text="Flagged automatically if recorded event timestamp is chronologically earlier than prior entries."
    )
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recorded_custody_events'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="System timestamp when this custody entry was submitted to the database."
    )

    class Meta:
        ordering = ['event_at', 'created_at']
        verbose_name = 'Custody Event'
        verbose_name_plural = 'Custody Events'

    def __str__(self):
        return f"{self.event_at:%Y-%m-%d %H:%M} [{self.event_type}] - {self.sample.sample_code}: {self.from_person} -> {self.to_person}"

    def clean(self):
        super().clean()
        if not self.from_person or not self.to_person:
            raise ValidationError("Both 'from person' and 'to person' must be specified for custody transfers.")

    def save(self, *args, **kwargs):
        # Auto-detect out of sequence: check if there's any custody event for this sample with event_at > this event_at
        if self.sample_id and self.event_at:
            later_events = CustodyEvent.objects.filter(
                sample_id=self.sample_id,
                event_at__gt=self.event_at
            )
            if self.pk:
                later_events = later_events.exclude(pk=self.pk)
            if later_events.exists():
                self.is_out_of_sequence = True
        super().save(*args, **kwargs)
