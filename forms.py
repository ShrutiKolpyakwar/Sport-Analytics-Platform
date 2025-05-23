from django import forms
from .models import Team

class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "sport"]  # Only these fields in the form
