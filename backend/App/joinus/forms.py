from django import forms
from .models import CV

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['pdf']

    def clean_pdf(self):
        pdf = self.cleaned_data['pdf']
        if not pdf.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        
    
        if pdf.size > 10 * 1024 * 1024:  # 10 MB in bytes
            raise forms.ValidationError('File size cannot exceed 10 MB.')
        
        return pdf
        