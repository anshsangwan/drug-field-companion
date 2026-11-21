from django import forms
from .models import ReviewRecord


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Provide comprehensive supervisor review comments. Required for both approvals and corrections.'
        }),
        error_messages={
            'required': 'A supervisory review comment is strictly mandatory.'
        }
    )

    class Meta:
        model = ReviewRecord
        fields = ['decision', 'comment']
        widgets = {
            'decision': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()
        if not comment:
            raise forms.ValidationError("A supervisory review comment is strictly mandatory.")
        if len(comment) < 5:
            raise forms.ValidationError("Please provide a descriptive comment explaining your supervisory decision.")
        return comment
