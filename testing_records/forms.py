from django import forms
from django.utils import timezone
from .models import TestEvent, TestKit, PRESUMPTIVE_DISCLAIMER


class TestEventForm(forms.ModelForm):
    performed_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Exact timestamp of test execution."
    )
    kit_expiry_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
        help_text="Expiration date indicated on test kit package."
    )

    class Meta:
        model = TestEvent
        fields = [
            'kit',
            'kit_lot_number',
            'kit_expiry_date',
            'performed_at',
            'observation_notes',
            'result_category',
            'limitations_note',
        ]
        widgets = {
            'kit': forms.Select(attrs={'class': 'form-select'}),
            'kit_lot_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., LOT-2025-88A'}),
            'observation_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objective sensory observations: e.g. Immediate deep purple reaction within 15 seconds...'
            }),
            'result_category': forms.Select(attrs={'class': 'form-select'}),
            'limitations_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Specify any ambient condition limitations, lighting constraints, or expired lot justification...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kit'].queryset = TestKit.objects.filter(active=True).order_by('name')
        if not self.instance.pk:
            self.initial['performed_at'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        result_category = cleaned_data.get('result_category')
        kit_expiry = cleaned_data.get('kit_expiry_date')
        performed_at = cleaned_data.get('performed_at')
        limitations = cleaned_data.get('limitations_note')

        valid_results = [choice[0] for choice in TestEvent.RESULT_CHOICES]
        if result_category and result_category not in valid_results:
            self.add_error('result_category', f"Invalid result category selected.")

        if kit_expiry and performed_at:
            performed_date = performed_at.date()
            if performed_date > kit_expiry and (not limitations or not limitations.strip()):
                self.add_error(
                    'limitations_note',
                    "The test kit is expired. You must provide an explicit justification in limitations notes."
                )

        return cleaned_data


class TestKitForm(forms.ModelForm):
    class Meta:
        model = TestKit
        fields = ['name', 'manufacturer', 'category', 'catalogue_reference', 'active', 'general_safety_note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cobalt Thiocyanate Presumptive Field Kit'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Forensic Diagnostics International'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Colorimetric Screening Ampoule'}),
            'catalogue_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CAT-CT-092'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'general_safety_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Standard PPE requirements and handling precautions. Do not enter chemical formulations.'
            }),
        }
