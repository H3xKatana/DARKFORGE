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
    

#admin form 
class SetPriceForm(forms.Form):
    price = forms.FloatField(label='New Price', min_value=0)


class EmailForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)