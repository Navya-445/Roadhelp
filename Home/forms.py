from django import forms
from django.contrib.auth.forms import AuthenticationForm

# forms.py


# Customer Signup Form
from .models import Customer, Mechanic

class CustomerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'mobile', 'address']

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.save()
        return customer


class MechanicSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Mechanic
        fields = ['username', 'password', 'mobile', 'skill']

    def save(self, commit=True):
        mechanic = super().save(commit=False)
        if commit:
            mechanic.save()
        return mechanic
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

    class Meta:
        model = MechanicProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'email', 'gender', 'profile_picture',
            'contact_no', 'aadhar_id', 'alternate_contact', 'experience', 'address', 
            'state', 'city', 'district', 'specialization'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # Date picker
            'gender': forms.Select(),
            'specialization': forms.Select()
        }

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

