from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


PRESUMPTIVE_DISCLAIMER = (
    "Field-test outcomes are presumptive screening results only. They do not establish the definitive "
    "identity of a substance. Confirmatory laboratory analysis is required."
)


class TestKit(models.Model):
    """
    Approved test kit catalogue reference.
    Contains descriptive commercial metadata only.
    Strictly prohibits chemical recipes, reagent quantities or procedural drug testing instructions.
    """
    name = models.CharField(max_length=255, help_text="Commercial kit or screening strip name.")
    manufacturer = models.CharField(max_length=255, help_text="Authorized manufacturing vendor.")
    category = models.CharField(
        max_length=128,
        help_text="Standardized test category (e.g., Colorimetric Field Screening, Lateral Flow Strip)."
    )
    catalogue_reference = models.CharField(
        max_length=128,
        unique=True,
        help_text="Unique vendor or institutional catalogue/part number."
    )
    active = models.BooleanField(
        default=True,
        help_text="Designates whether this kit model is currently active for field deployment."
    )
    general_safety_note = models.TextField(
        default="Wear nitrile gloves and safety eye protection. Ensure adequate ventilation. Dispose of used ampoules according to departmental biohazard protocols.",
        help_text="General handling precautions. Must not contain chemical formulas or production recipes."
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Test Kit'
        verbose_name_plural = 'Test Kits'

    def __str__(self):
        status = "Active" if self.active else "Inactive"
        return f"{self.name} ({self.catalogue_reference}) [{status}]"


class TestEvent(models.Model):
    """
    Documentation of an individual field presumptive testing event performed on a Sample.
    All results are classified strictly under standard presumptive categories.
    """
    RESULT_NOT_PERFORMED = 'Not performed'
    RESULT_INCONCLUSIVE = 'Inconclusive'
    RESULT_PRESUMPTIVE_POSITIVE = 'Presumptive positive'
    RESULT_PRESUMPTIVE_NEGATIVE = 'Presumptive negative'
    RESULT_INVALID_KIT_ISSUE = 'Invalid / Kit issue'

    RESULT_CHOICES = [
        (RESULT_NOT_PERFORMED, 'Not performed'),
        (RESULT_INCONCLUSIVE, 'Inconclusive'),
        (RESULT_PRESUMPTIVE_POSITIVE, 'Presumptive positive'),
        (RESULT_PRESUMPTIVE_NEGATIVE, 'Presumptive negative'),
        (RESULT_INVALID_KIT_ISSUE, 'Invalid / Kit issue'),
    ]

    sample = models.ForeignKey(
        'cases.Sample',
        on_delete=models.CASCADE,
        related_name='test_events'
    )
    kit = models.ForeignKey(
        TestKit,
        on_delete=models.PROTECT,
        related_name='test_events'
    )
    kit_lot_number = models.CharField(max_length=64, help_text="Batch or lot number printed on test kit.")
    kit_expiry_date = models.DateField(help_text="Manufacturer expiration date printed on packaging.")
    performed_at = models.DateTimeField(
        help_text="Timestamp when the presumptive test was executed."
    )
    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='conducted_tests'
    )
    observation_notes = models.TextField(
        help_text="Objective sensory observations (e.g. Color change observed after 30 seconds; faint line)."
    )
    result_category = models.CharField(
        max_length=64,
        choices=RESULT_CHOICES,
        help_text="Controlled screening outcome classification."
    )
    limitations_note = models.TextField(
        blank=True,
        default="",
        help_text="Operational limitations, ambient temperature notes, lighting issues, or expired lot override explanation."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-performed_at']
        verbose_name = 'Test Event'
        verbose_name_plural = 'Test Events'

    def __str__(self):
        return f"{self.sample.sample_code} - {self.kit.name} -> {self.result_category}"

    def clean(self):
        super().clean()
        valid_results = [choice[0] for choice in self.RESULT_CHOICES]
        if self.result_category and self.result_category not in valid_results:
            raise ValidationError({'result_category': f"Invalid result category '{self.result_category}'. Must be one of: {', '.join(valid_results)}"})

        if self.kit_expiry_date and self.performed_at:
            performed_date = self.performed_at.date() if hasattr(self.performed_at, 'date') else self.performed_at
            if performed_date > self.kit_expiry_date and not self.limitations_note:
                raise ValidationError({
                    'limitations_note': "The test kit is expired. You must provide an explicit justification in limitations notes."
                })
