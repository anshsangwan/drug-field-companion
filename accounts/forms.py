from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username or email',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
        })
    )


class UserCreateForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Field Officer', 'Field Officer (Case/Sample creation, testing, custody)'),
        ('Supervisor', 'Supervisor (Review, approvals, corrections, reports)'),
        ('Administrator', 'Administrator (Full user & system management)'),
        ('Read-only User', 'Read-only User (Audit and report viewing only)'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Initial password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm initial password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            role_name = self.cleaned_data['role']
            group, _ = Group.objects.get_or_create(name=role_name)
            user.groups.clear()
            user.groups.add(group)
            if role_name == 'Administrator':
                user.is_staff = True
                user.save(update_fields=['is_staff'])
        return user


class UserUpdateForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Field Officer', 'Field Officer'),
        ('Supervisor', 'Supervisor'),
        ('Administrator', 'Administrator'),
        ('Read-only User', 'Read-only User'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_group = self.instance.groups.first()
            if current_group:
                self.fields['role'].initial = current_group.name

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role_name = self.cleaned_data['role']
            group, _ = Group.objects.get_or_create(name=role_name)
            user.groups.clear()
            user.groups.add(group)
            user.is_staff = (role_name == 'Administrator')
            user.save(update_fields=['is_staff'])
        return user
