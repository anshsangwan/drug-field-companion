from django.db import models
from django.contrib.auth.models import User


class AuditEvent(models.Model):
    """
    Chronological audit trail for significant system and record events.
    Records actor, action type, target model, object ID, concise change summary,
    optional client IP and timestamp.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Created Record'),
        ('UPDATE', 'Updated Record'),
        ('SUBMIT', 'Submitted For Review'),
        ('REVIEW_APPROVED', 'Documentation Approved'),
        ('REVIEW_CHANGES_REQUESTED', 'Changes Requested'),
        ('CUSTODY_RECORDED', 'Custody Event Recorded'),
        ('TEST_RECORDED', 'Test Event Recorded'),
        ('EVIDENCE_UPLOAD', 'Evidence Uploaded'),
        ('USER_MANAGEMENT', 'User Account Modified'),
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
    ]

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_events'
    )
    action = models.CharField(max_length=64, choices=ACTION_CHOICES, db_index=True)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=64)
    summary = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Event'
        verbose_name_plural = 'Audit Events'

    def __str__(self):
        actor_name = self.actor.username if self.actor else 'System/Anonymous'
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {actor_name} -> {self.action} on {self.object_type}#{self.object_id}"
