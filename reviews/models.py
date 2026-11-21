from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ReviewRecord(models.Model):
    """
    Formal supervisory verification or correction record for a Case.
    Tracks decisions (Approved or Changes requested) and mandatory review feedback.
    """
    DECISION_APPROVED = 'Approved'
    DECISION_CHANGES_REQUESTED = 'Changes requested'

    DECISION_CHOICES = [
        (DECISION_APPROVED, 'Approve Documentation'),
        (DECISION_CHANGES_REQUESTED, 'Request Corrections / Return Case'),
    ]

    case = models.ForeignKey(
        'cases.CaseRecord',
        on_delete=models.CASCADE,
        related_name='review_records'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reviews_conducted'
    )
    decision = models.CharField(max_length=32, choices=DECISION_CHOICES)
    comment = models.TextField(
        help_text="Detailed feedback, instructions for required revisions, or approval endorsement."
    )
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reviewed_at']
        verbose_name = 'Review Record'
        verbose_name_plural = 'Review Records'

    def __str__(self):
        return f"{self.case.case_reference} -> {self.decision} by {self.reviewer.username} on {self.reviewed_at:%Y-%m-%d}"

    def clean(self):
        super().clean()
        if self.comment is not None and self.comment != '' and not self.comment.strip():
            raise ValidationError({'comment': "A supervisory review comment is strictly mandatory."})
