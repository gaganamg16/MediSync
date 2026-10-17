from django import forms
from .models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            "patient",
            "medicine_name",
            "dosage",
            "frequency",
            "instructions",
            "start_date",
            "end_date",
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "instructions": forms.Textarea(
                attrs={"rows": 3}
            ),
        }