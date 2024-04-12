# forms.py
from django import forms
from .models import CustomGame


class CustomGameForm(forms.ModelForm):
    class Meta:
        model = CustomGame
        exclude = ['user','price','payment','game_status','progression','progression']  # Exclude user field as we'll handle it separately
        widgets = {
            'genres': forms.CheckboxSelectMultiple,  # Use checkboxes for genre selection
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Make image field optional

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('image') and not cleaned_data.get('prototype_game'):
            raise forms.ValidationError("Either image or prototype game file is required.")
        return cleaned_data