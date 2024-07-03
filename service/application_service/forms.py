from django import forms
from .models import CandidateProfile, Application, Comment


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['name', 'last_name', 'education', 'experience', 'photo', 'phone_number', 'address']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'resume', 'cover_letter', 'comments', 'position', 'interview_date', 'feedback',
            'rating', 'portfolio_link', 'github_profile'
        ]

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['education', 'experience', 'photo', 'phone_number', 'address']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']        