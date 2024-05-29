# forms.py
from django import forms
from .models import CustomGame


class CustomGameForm(forms.ModelForm):
    class Meta:
        model = CustomGame
        exclude = ['user','price','payment','game_status','progression','progression','completed','platform','prototype','prototype_video_url','created_at','price','prototype']  # Exclude user field as we'll handle it separately
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Make image field optional
        self.fields['title'].widget.attrs['style'] = "isplay: block;width: 100%;margin-bottom: 25px;padding: 15px;border: none;border: 1px solid white;background-color: rgb(63 36 99);color: white;caret-color: var(--main-color);"
        self.fields['general_info'].widget.attrs['style'] = "isplay: block;width: 100%;margin-bottom: 25px;padding: 15px;border: none;border: 1px solid white;background-color: rgb(63 36 99);color: white;caret-color: var(--main-color);"
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