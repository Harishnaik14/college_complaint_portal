from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'category', 'subject', 'description', 'anonymous']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Describe your concern in detail'}),
            'anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '')
        return subject.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        return description.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip()
        return email


class AnnouncementForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement title'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Announcement details'})
    )
