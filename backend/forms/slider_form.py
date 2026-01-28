from django import forms
from backend.models import Slider


class SliderModelForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
