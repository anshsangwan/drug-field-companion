from django import forms
from django.conf import settings
from .models import EvidenceFile, validate_file_extension_and_size
from cases.models import Sample
import os


class EvidenceUploadForm(forms.ModelForm):
    class Meta:
        model = EvidenceFile
        fields = ['sample', 'file', 'caption']
        widgets = {
            'sample': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descriptive label: e.g. Tamper seal intact upon laboratory handover'
            }),
        }

    def __init__(self, *args, case=None, **kwargs):
        super().__init__(*args, **kwargs)
        if case:
            self.fields['sample'].queryset = case.samples.all()
            self.fields['sample'].empty_label = "General Case Evidence (No specific sample)"
        else:
            self.fields['sample'].queryset = Sample.objects.none()

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            validate_file_extension_and_size(uploaded_file)
            content_type = getattr(uploaded_file, 'content_type', '')
            allowed_mimes = getattr(settings, 'ALLOWED_EVIDENCE_MIME_TYPES', ['image/jpeg', 'image/png', 'application/pdf'])
            # Only validate mime if provided
            if content_type and content_type not in allowed_mimes and content_type != 'application/octet-stream':
                raise forms.ValidationError(f"Invalid MIME content type: '{content_type}'.")
        return uploaded_file
