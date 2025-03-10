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
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('customer_login')
    else:
        form = CustomerSignupForm()
    return render(request, 'customer_signup.html', {'form': form})


# Mechanic Signup View
def mechanic_signup(request):
    if request.method == 'POST':
        form = MechanicSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            mechanic = form.save(commit=False)
            mechanic.user = user
            mechanic.save()
            return redirect('mechanic_login')
    else:
        form = MechanicSignupForm()
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
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    customers = Customer.objects.all()
    mechanics = Mechanic.objects.all()
    return render(request, 'admin_dashboard.html', {'customers': customers, 'mechanics': mechanics})


# Approve/Reject Mechanic
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    customers = Customer.objects.all()
    mechanics = Mechanic.objects.all()
    return render(request, 'admin_dashboard.html', {'customers': customers, 'mechanics': mechanics})


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