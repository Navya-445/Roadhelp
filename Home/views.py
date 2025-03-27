from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Customer, Mechanic,MechanicNum
from .forms import CustomerSignupForm, MechanicSignupForm
from django.http import JsonResponse


# Create your views here.
def index1(request):
    
    return render(request, 'index1.html',)
def index(request):
    
    return render(request, 'index.html',)
def services(request):
    return render(request, 'services.html')
def Reg(request):
    return render(request, 're_all.html')
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:  # Check if the user is an admin
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("adminlogin")
    return render(request, "adminlogin.html")
def customer_signup(request):
    form = CustomerSignupForm()  # Initialize an empty form

    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request, 'Signup successful! Please <a href={% url \'mechaniclogout\' %}"style="color: blue; text-decoration: none; font-weight: bold;">log in</a>.')
            form = CustomerSignupForm()  # Reset the form after successful signup

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'customer_signup.html', {'form': form})

# Mechanic Signup View
import re
from django.urls import reverse

def mechanic_signup(request):
    form = MechanicSignupForm()  # Initialize an empty form

    if request.method == 'POST':
        form = MechanicSignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mobile = form.cleaned_data['mobile']

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken. Please choose another.')

            # Validate password length
            if len(password) < 8:
                form.add_error('password', 'Password must be at least 8 characters long.')

            # Validate mobile number format (+91xxxxxxxxxx)
            if not mobile.startswith('+91') or len(mobile) != 13 or not mobile[3:].isdigit():
                form.add_error('mobile', 'Enter a valid 10-digit mobile number with country code +91.')

            # If validation errors exist, show them
            if form.errors:
                return render(request, 'mechanic_signup.html', {'form': form})

            # Create user and mechanic profile
            user = User.objects.create_user(
                username=username,
                password=password
            )
            mechanic = form.save(commit=False)
            mechanic.user = user
            mechanic.save()

            # Display success message with logout button
            messages.success(request, f'''Signup successful! Your account has not been approved yet. 
                             You can <a href="{reverse('mechaniclogout')}" style="color: red; text-decoration: none; font-weight: bold;">Logout</a> now.''')
            form = MechanicSignupForm()  # Reset the form after successful signup

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'mechanic_signup.html', {'form': form})
# Customer Login View
def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'customer'):
            login(request, user)
            return redirect('customer_welcome')
        else:
            return render(request, 'customer_login.html', {'error': 'Invalid credentials or not a customer account'})
    return render(request, 'customer_login.html')


# Mechanic Login View
def mechanic_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'mechanic'):
            if user.mechanic.status:  # Check if approved by admin
                login(request, user)
                return redirect('mechanic_welcome')
            else:
                return render(request, 'mechanic_login.html', {'error': 'Your account is not approved yet'})
        else:
            return render(request, 'mechanic_login.html', {'error': 'Invalid credentials or not a mechanic account'})
    return render(request, 'mechanic_login.html')


# Customer Welcome Page
@login_required
def customer_welcome(request):
    return render(request, 'index.html')


# Mechanic Welcome Page
@login_required
def mechanic_welcome(request):
    return render(request, 'mechanic_welcome.html')


# Admin Dashboard View
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_dashboard(request):
#     customers = Customer.objects.all()
#     mechanics = Mechanic.objects.all()
#     return render(request, 'admin_dashboard.html', {'customers': customers, 'mechanics': mechanics})


# Approve/Reject Mechanic
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    customers = Customer.objects.all()
    mechanics = Mechanic.objects.all()
    return render(request, 'base_admin.html', {'customers': customers, 'mechanics': mechanics})


# Approve/Reject Mechanic
@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_mechanic(request, mechanic_id):
    mechanic = Mechanic.objects.get(id=mechanic_id)
    mechanic.status = True
    mechanic.save()
    return redirect('manage_mechanic')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_mechanic(request, mechanic_id):
    mechanic = Mechanic.objects.get(id=mechanic_id)
    mechanic.delete()
    return redirect('manage_mechanic')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_mechanic(request):
    # Fetch all mechanics to display in the table
    mechanics = Mechanic.objects.all()
    
    # Check if there's an approval request
    if 'approve' in request.GET:
        mechanic_id = request.GET.get('approve')
        mechanic = get_object_or_404(Mechanic, id=mechanic_id)
        mechanic.status = True
        mechanic.save()
        return redirect('manage_mechanic')  # Reload the page after approval
    
    # Check if there's a rejection request
    if 'reject' in request.GET:
        mechanic_id = request.GET.get('reject')
        mechanic = get_object_or_404(Mechanic, id=mechanic_id)
        mechanic.delete()
        return redirect('manage_mechanic')  # Reload the page after rejection

    # Render the page with mechanics and their status
    return render(request, 'manage_mechanic.html', {'mechanics': mechanics})



# Admin Dashboard View

def adminlogout(request):
    """Log out the user and redirect to the homepage."""
    logout(request)  # Log out the current user
    return redirect('registers')  # Redirect to the homepage
def customerlogout(request):
    """Log out the user and redirect to the homepage."""
    logout(request)  # Log out the current user
    return redirect('registers')  # Redirect to the homepage
def mechaniclogout(request):
    """Log out the user and redirect to the homepage."""
    logout(request)  # Log out the current user
    return redirect('registers')  # Redirect to the homepage
def registered_customers(request):
    customers = Customer.objects.all()  # Assuming `Customer` is the model
    return render(request, 'registered_customers.html', {'customers': customers})

def about(request):
    return render(request, 'about.html')
def service(request):
    return render(request, 'service.html')
def why(request):
    return render(request, 'why.html')

def customerlogout(request):
    """Log out the user and redirect to the homepage."""
    logout(request)  # Log out the current user
    return redirect('registers') 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceProvided, ServiceRequest
from .forms import ServiceRequestForm, ServiceProvidedForm

# Display list of available services
def service_list(request):
    services = ServiceProvided.objects.all()
    return render(request, 'service.html', {'services': services})

# View service details and submit request form
def service_detail(request, service_id):
    service = get_object_or_404(ServiceProvided, id=service_id)

    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Assign logged-in user
            service_request.service = service
            service_request.save()
            messages.success(request, "Request added successfully. We will contact you shortly!")
            return redirect('service_detail', service_id=service.id)
    else:
        form = ServiceRequestForm()

    return render(request, 'service_detail.html', {'service': service, 'form': form})

# Manage services (Add/Delete)
@login_required
def manage_service(request):
    form = ServiceProvidedForm()  # Ensure form is always initialized
    services = ServiceProvided.objects.all()  

    if request.method == "POST":
        if "delete" in request.POST:
            service_id = request.POST.get("service_id")
            ServiceProvided.objects.filter(id=service_id).delete()
            messages.success(request, "Service deleted successfully!")
            return redirect('manage_service')  # Redirect to prevent re-submission

        else:
            form = ServiceProvidedForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Service added successfully!")
                return redirect('manage_service')  

    return render(request, 'manage_service.html', {'form': form, 'services': services})


@login_required
def view_requests(request):
    requests = ServiceRequest.objects.all()  # Fetch all service requests
    return render(request, 'view_requests.html', {'requests': requests})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MechanicProfile
from .forms import MechanicProfileForm

def complete_profile(request):
    """ Allows a mechanic to complete their profile. Redirects to View Profile once saved. """
    mechanic_profile, created = MechanicProfile.objects.get_or_create(user=request.user)

    if not created and mechanic_profile.first_name:  # Profile already exists
        return redirect('view_profile')

    if request.method == 'POST':
        form = MechanicProfileForm(request.POST, request.FILES, instance=mechanic_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been saved successfully.")
            return redirect('view_profile')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")

    else:
        form = MechanicProfileForm(instance=mechanic_profile)

    return render(request, 'complete_profile.html', {'form': form})

def view_profile(request):
    """ Displays Mechanic Profile with an option to Edit """
    mechanic_profile = get_object_or_404(MechanicProfile, user=request.user)
    return render(request, 'view_profile.html', {'profile': mechanic_profile})

def edit_profile(request):
    """ Allows the mechanic to edit their existing profile """
    mechanic_profile = get_object_or_404(MechanicProfile, user=request.user)

    if request.method == 'POST':
        form = MechanicProfileForm(request.POST, request.FILES, instance=mechanic_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('view_profile')

    else:
        form = MechanicProfileForm(instance=mechanic_profile)

    return render(request, 'edit_profile.html', {'form': form})


from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser) 
def view_mechdetails(request):
    """ Only superuser (admin) can view mechanic details """
    mechanics = MechanicProfile.objects.all()
    return render(request, 'view_mechdetails.html', {'mechanics': mechanics})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import TaskAssignment, ServiceRequest, MechanicProfile
from .forms import TaskAssignmentForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ServiceRequest, MechanicProfile, TaskAssignment
from .forms import TaskAssignmentForm

# Admin Task Assignment View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import ServiceRequest, MechanicProfile, TaskAssignment
from django.db.models import Exists, OuterRef

@user_passes_test(lambda u: u.is_superuser)  # Restrict to admin
def assign_task(request):
    # ✅ Ensure we fetch only unassigned service requests
    service_requests = ServiceRequest.objects.annotate(
        is_assigned=Exists(TaskAssignment.objects.filter(service_request=OuterRef('id')))
    ).filter(is_assigned=False)  # Shows only unassigned service requests

    districts = MechanicProfile.objects.values_list('district', flat=True).distinct()

    if request.method == "POST":
        service_request_id = request.POST.get('service_request_id')
        mechanic_id = request.POST.get('mechanic')

        service_request = get_object_or_404(ServiceRequest, id=service_request_id)
        mechanic = get_object_or_404(MechanicProfile, id=mechanic_id)

        # ❌ Prevent re-assigning if already assigned
        if TaskAssignment.objects.filter(service_request=service_request).exists():
            messages.warning(request, "This service request is already assigned!")
            return redirect('assign_task')

        # ✅ Assign Task
        task = TaskAssignment.objects.create(
            user=service_request.user,
            service_request=service_request,
            mechanic=mechanic,
            status="Pending"
        )

        messages.success(request, "Task Assigned Successfully!")

        # ✅ Stay on the same page and list assigned tasks
        return redirect('assign_task')

    # ✅ Fetch already assigned tasks
    assigned_tasks = TaskAssignment.objects.select_related('service_request', 'mechanic')

    return render(request, 'assign_task.html', {
        'service_requests': service_requests,
        'districts': districts,
        'assigned_tasks': assigned_tasks  # ✅ Pass assigned tasks to template
    })

@login_required
def my_appointments(request):
    mechanic_profile = get_object_or_404(MechanicProfile, user=request.user)
    assigned_tasks = TaskAssignment.objects.filter(mechanic=mechanic_profile)

    return render(request, 'my_appointments.html', {
        'assigned_tasks': assigned_tasks
    })

def view_task_details(request):
    tasks = TaskAssignment.objects.all()  # Fetch all assigned tasks
    return render(request, "view_tasks.html", {"tasks": tasks})

def edit_task_status(request, task_id):
    task = get_object_or_404(TaskAssignment, id=task_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()
        messages.success(request, "Task status updated successfully!")
        return redirect('view_task_details')  # Redirects to task list

    return render(request, 'edit_task_status.html', {'task': task})


# ✅ AJAX Function - Fetch Mechanics by District
def get_mechanics_by_district(request):
    district = request.GET.get('district')
    mechanics = MechanicProfile.objects.filter(district=district).values('id', 'first_name', 'last_name', 'specialization__name')
    return JsonResponse(list(mechanics), safe=False)
# Customer Dashboard: View My Service Requests
@login_required
def my_requests(request):
    customer_tasks = TaskAssignment.objects.filter(user=request.user).select_related('service_request__service', 'mechanic')
    
    # Fetch the first stored mechanic number (Modify this logic if needed)
    mechanic = MechanicNum.objects.first()

    return render(request, 'my_requests.html', {
        'customer_tasks': customer_tasks,
        'mechanic': mechanic
    })
from .forms import ContactForm
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to contact page after submission
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
def admin_contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, "admin_contact.html", {"messages": messages})


# @user_passes_test(lambda u: u.is_superuser)
# def send_messagemech(request):
#     return render(request,"send_notif.html")

@user_passes_test(lambda u: u.is_superuser)  # Only admin can access
def see_taskdetails(request):
    assigned_tasks = TaskAssignment.objects.select_related('mechanic', 'service_request', 'user').all()

    return render(request, 'send_notif.html', {'assigned_tasks': assigned_tasks})

@user_passes_test(lambda u: u.is_superuser)
def approve_msg(request):
    # Fetch all approved mechanics
    approved_mechanics = Mechanic.objects.filter(status=True)

    return render(request, 'send_approvealerts.html', {'approved_mechanics': approved_mechanics})
def notification_menu(request):
    return render(request, 'menu.html')


def task_details(request, task_id):
    task = get_object_or_404(TaskAssignment, id=task_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()
        messages.success(request, "Task status updated successfully!")
        return redirect('task_details', task_id=task.id)  # ✅ Stay on the same page

    return render(request, "task_details.html", {"task": task})
from .models import  TaskAssignment
from .models import MechanicTaskUpdate
from .forms import WorkDetailsForm,TaskStatusUpdateForm
from .models import StatusUpdate, TaskAssignment
from .forms import StatusUpdateForm

@login_required
def mechanic_assigned_tasks(request):
    """Mechanic views their assigned tasks with latest status updates"""
    
    assigned_tasks = TaskAssignment.objects.filter(mechanic=request.user.mechanicprofile)

    # Fetch latest status update for each task
    for task in assigned_tasks:
        latest_status_update = StatusUpdate.objects.filter(task=task).order_by('-updated_at').first()
        task.latest_status = latest_status_update.status if latest_status_update else "Pending"  # Default to Pending

    return render(request, 'mechanic_assigned_tasks.html', {'assigned_tasks': assigned_tasks})

@login_required
def update_mechanic_task_status(request, task_id):
    """Mechanic updates task status"""
    
    task = get_object_or_404(TaskAssignment, id=task_id)
    service_request = task.service_request  # Ensure this field exists in TaskAssignment model

    # Fetch or create a status update entry
    task_update, created = StatusUpdate.objects.get_or_create(
        task=task, 
        mechanic=request.user.mechanicprofile,
        service_request=service_request  
    )

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=task_update)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Task status updated successfully!")
            return redirect('mechanic_assigned_tasks')  # Redirect to assigned tasks
    else:
        form = StatusUpdateForm(instance=task_update)

    return render(request, 'update_task_status.html', {'form': form, 'task_update': task_update})

from .models import MechanicDetailsFill, TaskAssignment
from .forms import MechanicWorkDetailsForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TaskAssignment, MechanicDetailsFill,SparePart
from .forms import MechanicWorkDetailsForm

def mechanic_work_details(request):
    """View listing assigned tasks with a Complete button"""
    assigned_tasks = TaskAssignment.objects.filter(mechanic=request.user.mechanicprofile)
    return render(request, 'workdetails.html', {'assigned_tasks': assigned_tasks})

def fill_mechanic_details(request, task_id):
    """View for mechanics to fill work details"""
    task = get_object_or_404(TaskAssignment, id=task_id)

    # Check if details already exist or create a new entry
    mechanic_details, created = MechanicDetailsFill.objects.get_or_create(
        task=task, 
        mechanic=request.user.mechanicprofile, 
        service_request=task.service_request
    )

    if request.method == "POST":
        form = MechanicWorkDetailsForm(request.POST, request.FILES, instance=mechanic_details)
        
        if form.is_valid():
            work_details = form.save(commit=False)
            work_details.before_image = form.cleaned_data.get('before_image')
            work_details.after_image = form.cleaned_data.get('after_image')
            work_details.mechanic_notes = form.cleaned_data.get('mechanic_notes')
            
            # ✅ Assign spare parts correctly
            selected_parts = form.cleaned_data.get('used_spare_parts')

            if "not_used" in selected_parts:  
                work_details.used_spare_parts.clear()  # ✅ If "Not Used" is selected, remove previous selections
            else:
                spare_part_objects = SparePart.objects.filter(id__in=selected_parts)
                work_details.used_spare_parts.set(spare_part_objects)  # ✅ Assign multiple spare parts

            # ✅ Save the updated work details
            work_details.save()

            # messages.success(request, "Work details successfully submitted.")
            return render(request, 'success_message.html', {'task': task})   # ✅ Redirect instead of rendering directly

        else:
            messages.error(request, "There was an error in the form. Please check your inputs.")

    else:
        form = MechanicWorkDetailsForm(instance=mechanic_details)

    return render(request, 'fill_details.html', {'form': form, 'task': task})

from .models import Feedback, ServiceRequest
from .forms import FeedbackForm


@login_required
def feedback_list(request):
    """ List all service requests for feedback submission for the logged-in user """
    
    # Fetch only tasks assigned to the logged-in customer
    customer_tasks = TaskAssignment.objects.filter(
        service_request__user=request.user
    ).select_related('service_request__service', 'mechanic')

    # Add feedback status for each task
    for task in customer_tasks:
        task.is_feedback_completed = Feedback.objects.filter(service_request=task.service_request).exists()

    return render(request, 'feedback_list.html', {
        'customer_tasks': customer_tasks
    })
@login_required
def fill_feedback(request, service_request_id):
    service_request = get_object_or_404(ServiceRequest, id=service_request_id)
    task_assignment = TaskAssignment.objects.filter(service_request=service_request).first()

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.service_request = service_request
            feedback.mechanic = task_assignment.mechanic if task_assignment else None  # Ensure mechanic exists
            feedback.user = request.user  # Assign the logged-in user
            feedback.save()
            # messages.success(request, "Feedback submitted successfully!")
            return render(request, "feedback_success.html")
            
            
            # ✅ Redirect to the feedback list page instead of rendering another template
            # return redirect("feedback_list")  

    else:
        form = FeedbackForm()

    return render(request, "fill_feedback.html", {"form": form, "service_request": service_request})
def view_byadmin(request, mechanic_id):
    """ Fetch and display a single mechanic's full profile """
    mechanic = get_object_or_404(MechanicProfile, id=mechanic_id)

    return render(request, 'view_byadmin.html', {'mechanic': mechanic})

import razorpay
from django.conf import settings
from django.shortcuts import render
from .models import ServiceRequest, PriceList

def payment_page(request):
    """ Fetch service requests and corresponding prices for the logged-in user and generate Razorpay orders """
    
    customer_tasks = ServiceRequest.objects.filter(user=request.user).select_related('service')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    customer_tasks_with_prices = []
    
    for task in customer_tasks:
        price_entry = PriceList.objects.filter(service=task.service).first()
        amount_inr = price_entry.amount_inr if price_entry else None  # Ensure the amount is valid

        if amount_inr:
            # Convert amount to paisa (Razorpay requires the amount in paisa)
            amount_paisa = int(amount_inr * 100)

            # Create a Razorpay order
            order_data = {
                "amount": amount_paisa,
                "currency": "INR",
                "payment_capture": 1,  # Auto capture payment
            }
            order = client.order.create(order_data)

            customer_tasks_with_prices.append({
                'task': task,
                'service': task.service,
                'amount_inr': amount_inr,
                'order_id': order['id'],  # Send Razorpay order ID to frontend
            })

    return render(request, 'payment_page.html', {
        'customer_tasks': customer_tasks_with_prices,
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,  # Pass key to frontend
    })
from django.shortcuts import render

def payment_success(request):
    return render(request, 'payment_success.html')

# from .models import ServiceRequest, PriceList
# def payment_page(request):
#     """ Fetch service requests and corresponding prices for the logged-in user """
#     customer_tasks = ServiceRequest.objects.filter(user=request.user).select_related('service')

#     # Create a list to store tasks with their corresponding prices
#     customer_tasks_with_prices = []

#     for task in customer_tasks:
#         price_entry = PriceList.objects.filter(service=task.service).first()  # Fetch the first price entry for the service
#         amount_inr = price_entry.amount_inr if price_entry else "Not Available"

#         customer_tasks_with_prices.append({
#             'task': task,
#             'service': task.service,
#             'amount_inr': amount_inr
#         })

#     return render(request, 'payment_page.html', {'customer_tasks': customer_tasks_with_prices})

# def add_status(request):
#     return render(request,"update_task_status.html")
# @login_required
# def assigned_tasks(request):
#     """Mechanic views their assigned tasks (appointments)."""
#     assigned_tasks = MechanicTaskUpdate.objects.filter(mechanic=request.user)
    
#     return render(request, 'mechanic_assigned_tasks.html', {'assigned_tasks': assigned_tasks})

# @login_required
# def update_mechanic_task_status(request, task_id):
#     """Mechanic updates task status"""
#     task_update = get_object_or_404(MechanicTaskUpdate, id=task_id, mechanic=request.user)
    
#     if request.method == 'POST':
#         form = TaskStatusUpdateForm(request.POST, instance=task_update)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Task status updated successfully!")
#             return redirect('mechanic_assigned_tasks')  # Redirect to assigned tasks page
#     else:
#         form = TaskStatusUpdateForm(instance=task_update)

#     return render(request, 'update_task_status.html', {'form': form, 'task_update': task_update})

# # @login_required
# # @login_required
# def add_status(request, task_id):
#     """View to update task status only"""
#     task = get_object_or_404(MechanicTaskUpdate, task__id=task_id)

#     if request.method == 'POST':
#         form = TaskStatusUpdateForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('work_details_filling', task_id=task.task.id)  # Redirect to work details filling
#     else:
#         form = TaskStatusUpdateForm(instance=task)

#     return render(request, 'add_status.html', {'form': form, 'task': task})


# @login_required
# def work_details_filling(request, task_id):
#     """View to allow mechanics to fill in work details"""
#     task = get_object_or_404(MechanicTaskUpdate, task__id=task_id)

#     if request.method == 'POST':
#         form = WorkDetailsForm(request.POST, request.FILES, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('work_history')  # Redirect to work history after completion
#     else:
#         form = WorkDetailsForm(instance=task)

#     return render(request, 'work_details.html', {'form': form, 'task': task}) 

# @login_required
# def work_history(request):
#     """View to display completed tasks history"""
#     completed_tasks = MechanicTaskUpdate.objects.filter(status='Completed').order_by('-task__assigned_date')

#     return render(request, 'work_history.html', {'completed_tasks': completed_tasks})




# # Admin Task Assignment View
# @user_passes_test(lambda u: u.is_superuser)  # Restrict to admin
# def assign_task(request):
#     service_requests = ServiceRequest.objects.all()
#     mechanics = MechanicProfile.objects.filter(user__mechanic__status=True)
#     selected_district = None
#     filtered_mechanics = None

#     if request.method == "POST":
#         service_request_id = request.POST.get('service_request')
#         selected_district = request.POST.get('district')  # Get selected district
#         mechanic_id = request.POST.get('mechanic')

#         # Filter mechanics by selected district
#         if selected_district:
#             filtered_mechanics = mechanics.filter(district=selected_district)

#         if mechanic_id:
#             service_request = get_object_or_404(ServiceRequest, id=service_request_id)
#             mechanic = get_object_or_404(MechanicProfile, id=mechanic_id)

#             task = TaskAssignment.objects.create(
#                 user=service_request.user,
#                 service_request=service_request,
#                 mechanic=mechanic
#             )
#             task.save()
#             return redirect('assign_task')

#     return render(request, 'assign_task.html', {
#         'service_requests': service_requests,
#         'mechanics': mechanics,
#         'selected_district': selected_district,
#         'filtered_mechanics': filtered_mechanics
#     })

# # Mechanic Dashboard: View Assigned Appointments
# @login_required
# def my_appointments(request):
#     mechanic_profile = get_object_or_404(MechanicProfile, user=request.user)
#     assigned_tasks = TaskAssignment.objects.filter(mechanic=mechanic_profile)

#     return render(request, 'my_appointments.html', {
#         'assigned_tasks': assigned_tasks
#     })

# # Customer Dashboard: View My Service Requests
# @login_required
# def my_requests(request):
#     customer_tasks = TaskAssignment.objects.filter(user=request.user)

#     return render(request, 'my_requests.html', {
#         'customer_tasks': customer_tasks
#     })