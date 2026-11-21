from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import CaseRecord, Sample


class CaseRecordForm(forms.ModelForm):
    incident_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Select or specify date and time of incident occurrence."
    )

    class Meta:
        model = CaseRecord
        fields = ['title', 'incident_datetime', 'general_location', 'description', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Highway 101 Vehicle Stop Field Screening'}),
            'general_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Sector 4 Commercial Port Facility'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide operational background and circumstances of field inspection...'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_to'].required = False
        if self.instance and self.instance.incident_datetime:
            self.initial['incident_datetime'] = self.instance.incident_datetime.strftime('%Y-%m-%dT%H:%M')


class SampleForm(forms.ModelForm):
    collected_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Date and time specimen was secured in the field."
    )
    sample_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to auto-generate (e.g. SMP-2026-0001)'}),
        help_text="Unique specimen identifier. Auto-generated if left blank."
    )

    class Meta:
        model = Sample
        fields = ['sample_code', 'collected_at', 'description', 'packaging_reference', 'seal_reference', 'initial_condition']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Physical description of material, color, packaging state...'}),
            'packaging_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Heavy-gauge evidence pouch #A-402'}),
            'seal_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., SEAL-NUM-7719'}),
            'initial_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Intact, Dry, Double-bagged'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.collected_at:
            self.initial['collected_at'] = self.instance.collected_at.strftime('%Y-%m-%dT%H:%M')

    def clean_sample_code(self):
        code = self.cleaned_data.get('sample_code')
        if code:
            code = code.strip()
            qs = Sample.objects.filter(sample_code=code)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f"Sample code '{code}' is already registered. Codes must be strictly unique.")
        return code
