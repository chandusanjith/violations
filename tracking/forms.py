# forms.py
from django import forms
from .models import Violation, ViolationType
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ViolationForm(forms.ModelForm):
    class Meta:
        model = Violation
        fields = ['date', 'violation_type', 'fine_collected', 'description', 'vehicle_number', 'officer_name', 'image']
        widgets = {
            'officer_name': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    violation_type = forms.ModelChoiceField(queryset=ViolationType.objects.all(), empty_label="Select Violation Type")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ViolationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['officer_name'].initial = user.get_full_name()
        self.fields['date'].initial = timezone.now().date()