# disasters/forms.py

from django import forms
from .models import DisasterEvent, Report, Resource, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .utils import format_phone_number
class DisasterEventForm(forms.ModelForm):
    class Meta:
        model = DisasterEvent
        fields = ['name', 'event_type', 'date_occurred', 'location', 'description'] #'latitude', 'longitude'
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
class ReportForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=DisasterEvent.objects.all(), empty_label="Select Event")
    class Meta:
        model = Report
        fields = ['event', 'reporter_name', 'contact_info', 'details']

class ResourceForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=DisasterEvent.objects.all(), empty_label="Select Event")
    class Meta:
        model = Resource
        fields = ['event', 'resource_type', 'quantity']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        formatted_phone_number = format_phone_number(phone_number)
        if not formatted_phone_number:
            raise forms.ValidationError("Invalid phone number format.")
        return formatted_phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'location', 'birth_date', 'phone_number']