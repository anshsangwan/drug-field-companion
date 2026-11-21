from django import forms
from django.utils import timezone
from .models import CustodyEvent


class CustodyEventForm(forms.ModelForm):
    event_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Exact timestamp when physical custody transfer occurred."
    )

    class Meta:
        model = CustodyEvent
        fields = [
            'event_type',
            'event_at',
            'from_person',
            'to_person',
            'location_reference',
            'seal_reference',
            'remarks',
        ]
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'from_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Det. J. Vance (Badge #409)'}),
            'to_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Evidence Custodian M. Ramirez (Badge #112)'}),
            'location_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Central Evidence Locker #4B'}),
            'seal_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., SEAL-RED-9904'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Transfer context, condition confirmation, or storage reasons...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['event_at'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
