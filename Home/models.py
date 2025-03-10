from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    skill = models.CharField(max_length=100)
    status = models.BooleanField(default=False)  # Approval status by admin

    def __str__(self):
        return self.user.username
    
class ServiceProvided(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='services/')  # Main picture
    short_description = models.TextField()
    long_description = models.TextField()
    points_to_remember = models.TextField()
    additional_picture = models.ImageField(upload_to='services/', blank=True, null=True)  # Additional Picture

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Logged-in user
    service = models.ForeignKey(ServiceProvided, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    vehicle_reg_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Request from {self.user.username} for {self.service.name}"
    

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links profile to User
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True) 
    email = models.EmailField(unique=True)
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    profile_picture = models.ImageField(upload_to='mechanic_profiles/', null=True, blank=True)

    # Mobile Number Validation (10 Digits)
    contact_no = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid number ")],
        unique=True
    )

    # Aadhar Number Validation (12 Digits)
    aadhar_id = models.CharField(
        max_length=12, 
        validators=[RegexValidator(regex=r'^\d{12}$', message="Aadhar number must be exactly 12 digits")], 
        unique=True
    )

    alternate_contact = models.CharField(max_length=15, blank=True, null=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

    # Fetching Name from ServiceProvided Model
    specialization = models.ForeignKey('ServiceProvided', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

from django.db import models
from django.contrib.auth.models import User

class TaskAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer
    service_request = models.ForeignKey('ServiceRequest', on_delete=models.CASCADE)
    mechanic = models.ForeignKey('MechanicProfile', on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    status_choices = [('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return f"Task for {self.user.username} assigned to {self.mechanic.first_name}"


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
class MechanicNum(models.Model):
    Mob_num = models.CharField(max_length=15)

    def __str__(self):
        return self.Mob_num

