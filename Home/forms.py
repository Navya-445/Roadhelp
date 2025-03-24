from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
# forms.py


# Customer Signup Form
from .models import Customer, Mechanic
class CustomerSignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z][A-Za-z0-9]*$',  
                message="Username must start with a letter and contain only letters and numbers."
            )
        ]
    )
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and special character."
            )
        ]
    )
    mobile = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+\d{1,4}\d{10}$',
                message="Enter a valid mobile number with country code (e.g., +911234567890)."
            )
        ]
    )
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'mobile', 'address']
import re
class MechanicSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    mobile = forms.CharField(max_length=13, initial='+91')  # Default +91
    SKILL_CHOICES = [
        ('car_repair', 'Car Repair Expert'),
        ('bike_service', 'Bike Service Expert'),
    ]
    skill = forms.ChoiceField(choices=SKILL_CHOICES, required=True)

    class Meta:
        model = Mechanic
        fields = ['username', 'password', 'mobile', 'skill']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.startswith('+91') or len(mobile) != 13 or not mobile[3:].isdigit():
            raise forms.ValidationError("Enter a valid 10-digit mobile number with country code +91.")
        return mobile
from django import forms
from .models import ServiceProvided, ServiceRequest

class ServiceProvidedForm(forms.ModelForm):
    class Meta:
        model = ServiceProvided
        fields = ['name', 'picture', 'short_description', 'long_description', 'points_to_remember', 'additional_picture']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        exclude = ['user', 'service']  # Auto-assign user & service
from django import forms
from django import forms
from .models import MechanicProfile, ServiceRequest, TaskAssignment

# List of Kerala Districts
KERALA_DISTRICTS = [
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Kollam', 'Kollam'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Alappuzha', 'Alappuzha'),
    ('Kottayam', 'Kottayam'),
    ('Idukki', 'Idukki'),
    ('Ernakulam', 'Ernakulam'),
    ('Thrissur', 'Thrissur'),
    ('Palakkad', 'Palakkad'),
    ('Malappuram', 'Malappuram'),
    ('Kozhikode', 'Kozhikode'),
    ('Wayanad', 'Wayanad'),
    ('Kannur', 'Kannur'),
    ('Kasaragod', 'Kasaragod'),
]

class MechanicProfileForm(forms.ModelForm):
    district = forms.ChoiceField(choices=KERALA_DISTRICTS, label="District")
    contact_no = forms.CharField(
        max_length=13, 
        initial='+91', 
        label="Contact Number"
    )
    alternate_contact = forms.CharField(
        max_length=13, 
        required=False, 
        initial='+91', 
        label="Alternate Contact Number"
    )

    class Meta:
        model = MechanicProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'email', 'gender', 'profile_picture',
            'contact_no', 'aadhar_id', 'alternate_contact', 'experience', 'address', 
            'state', 'city', 'district', 'specialization'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'specialization': forms.Select()
        }

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.startswith('+91') or len(contact_no) != 13 or not contact_no[3:].isdigit():
            raise forms.ValidationError("Enter a valid 10-digit mobile number with country code +91.")
        return contact_no

    def clean_alternate_contact(self):
        alternate_contact = self.cleaned_data.get('alternate_contact')
        if alternate_contact and (not alternate_contact.startswith('+91') or len(alternate_contact) != 13 or not alternate_contact[3:].isdigit()):
            raise forms.ValidationError("Enter a valid 10-digit mobile number with country code +91.")
        return alternate_contact
class ServiceRequestForm(forms.ModelForm):
    state = forms.CharField(initial="Kerala", disabled=True)  # Pre-filled, read-only

    class Meta:
        model = ServiceRequest
        exclude = ['user', 'service']

class TaskAssignmentForm(forms.ModelForm):
    district = forms.ChoiceField(choices=KERALA_DISTRICTS, label="Select District")
    mechanic = forms.ModelChoiceField(
        queryset=MechanicProfile.objects.none(),  
        label="Mechanic - Specialization"
    )

    class Meta:
        model = TaskAssignment
        fields = ['service_request', 'mechanic', 'status']

    def __init__(self, *args, **kwargs):
        super(TaskAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['mechanic'].queryset = MechanicProfile.objects.none()

    def update_mechanics(self, district):
        """Dynamically update the mechanic dropdown based on district selection."""
        self.fields['mechanic'].queryset = MechanicProfile.objects.filter(district=district)

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']

from django import forms
from .models import MechanicTaskUpdate, SparePart

class TaskStatusUpdateForm(forms.ModelForm):
    """Form to update only the task status"""
    class Meta:
        model = MechanicTaskUpdate
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class WorkDetailsForm(forms.ModelForm):
    """Form to update work details, including times, notes, and images"""
    class Meta:
        model = MechanicTaskUpdate
        fields = [
            'location_reached_time', 'service_completed_time',
            'before_service_picture', 'after_service_picture',
            'mechanic_notes', 'spare_parts_used'
        ]
        widgets = {
            'location_reached_time': forms.Select(attrs={'class': 'form-control'}),
            'service_completed_time': forms.Select(attrs={'class': 'form-control'}),
            'mechanic_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'spare_parts_used': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class SparePartForm(forms.ModelForm):
    """Form for spare parts selection while updating work details"""
    class Meta:
        model = SparePart
        fields = ['name', 'stock_quantity']
from .models import StatusUpdate

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['status', 'remarks']

from .models import MechanicDetailsFill

from datetime import datetime
from django import forms
from .models import MechanicDetailsFill, SparePart

class MechanicWorkDetailsForm(forms.ModelForm):
    """Form for mechanics to fill work details"""

    SPARE_PART_CHOICES = [(part.id, part.name) for part in SparePart.objects.all()]
    SPARE_PART_CHOICES.insert(0, ("not_used", "Not Used"))  # ✅ Add "Not Used" as an option

    used_spare_parts = forms.MultipleChoiceField(
        choices=SPARE_PART_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
    )

    class Meta:
        model = MechanicDetailsFill
        fields = [
            'completed_date', 'reached_time', 'finished_time', 
            'before_image', 'after_image', 'used_spare_parts', 'mechanic_notes'
        ]
        widgets = {
            'completed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reached_time': forms.Select(attrs={'class': 'form-control'}),
            'finished_time': forms.Select(attrs={'class': 'form-control'}),
            'before_image': forms.FileInput(attrs={'class': 'form-control'}),
            'after_image': forms.FileInput(attrs={'class': 'form-control'}),
            'mechanic_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        """Validate time selection and auto-calculate total duration"""
        cleaned_data = super().clean()
        reached_time = cleaned_data.get("reached_time")
        finished_time = cleaned_data.get("finished_time")

        if reached_time and finished_time:
            try:
                # Ensure the format is correct before parsing
                start_time = datetime.strptime(reached_time, "%I:%M %p")
                end_time = datetime.strptime(finished_time, "%I:%M %p")

                # Allow midnight crossing
                if end_time < start_time:
                    end_time = end_time.replace(day=start_time.day + 1)

                # Validate that the difference is not zero
                if start_time == end_time:
                    self.add_error('finished_time', "Start time and end time cannot be the same.")
            except ValueError:
                self.add_error('finished_time', "Invalid Time Format.")

        return cleaned_data
