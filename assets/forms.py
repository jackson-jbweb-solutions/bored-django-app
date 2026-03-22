from django import forms

from .models import Cushion, Ward, Wheelchair

_INPUT = {"class": "form-input"}
_SELECT = {"class": "form-input"}
_TEXTAREA = {"class": "form-input", "rows": 2}
_DATE = {"class": "form-input", "type": "date"}


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={**_INPUT, "placeholder": "Ward name..."}),
        }


class CushionForm(forms.ModelForm):
    class Meta:
        model = Cushion
        fields = ["serial_number", "make", "model", "purchase_date", "notes", "status", "ward"]
        widgets = {
            "serial_number": forms.TextInput(attrs={**_INPUT, "placeholder": "Serial number..."}),
            "make": forms.TextInput(attrs={**_INPUT, "placeholder": "Make..."}),
            "model": forms.TextInput(attrs={**_INPUT, "placeholder": "Model..."}),
            "purchase_date": forms.DateInput(attrs=_DATE),
            "notes": forms.Textarea(attrs={**_TEXTAREA, "placeholder": "Notes..."}),
            "status": forms.Select(attrs=_SELECT),
            "ward": forms.Select(attrs=_SELECT),
        }


class WheelchairForm(forms.ModelForm):
    class Meta:
        model = Wheelchair
        fields = [
            "serial_number", "make", "model", "purchase_date",
            "notes", "status", "ward", "paired_cushion",
        ]
        widgets = {
            "serial_number": forms.TextInput(attrs={**_INPUT, "placeholder": "Serial number..."}),
            "make": forms.TextInput(attrs={**_INPUT, "placeholder": "Make..."}),
            "model": forms.TextInput(attrs={**_INPUT, "placeholder": "Model..."}),
            "purchase_date": forms.DateInput(attrs=_DATE),
            "notes": forms.Textarea(attrs={**_TEXTAREA, "placeholder": "Notes..."}),
            "status": forms.Select(attrs=_SELECT),
            "ward": forms.Select(attrs=_SELECT),
            "paired_cushion": forms.Select(attrs=_SELECT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["paired_cushion"].queryset = (
                Cushion.objects.filter(wheelchair__isnull=True)
                | Cushion.objects.filter(wheelchair=self.instance)
            )
        else:
            self.fields["paired_cushion"].queryset = Cushion.objects.filter(
                wheelchair__isnull=True
            )
