from django.urls import path,include
from . import views

urlpatterns = [
   
    path('',views.index1,name='home'),
    path('services',views.services,name='services'),
    path('customer_welcome/index.html',views.index,name='custlog'),
    path('customer_welcome/about.html',views.about,name='about'),
    path("cust-logout/", views.customerlogout, name="customerlogout"),
    path('customer_welcome/service.html',views.service_list,name='service'),
    path('customer_welcome/why.html',views.why,name='why'),
    path('customer_welcome/contact.html',views.contact,name='contact'),
    path('services',views.service_list,name='services'),
    path('register',views.Reg,name='registers'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path("admin-logout/", views.adminlogout, name="adminlogout"),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('mechanic_signup/', views.mechanic_signup, name='mechanic_signup'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('mechanic_login/', views.mechanic_login, name='mechanic_login'),
    path('customer_welcome/', views.customer_welcome, name='customer_welcome'),
    path('mechanic_welcome/', views.mechanic_welcome, name='mechanic_welcome'),
    path('approve_mechanic/<int:mechanic_id>/', views.approve_mechanic, name='approve_mechanic'),
    path('reject_mechanic/<int:mechanic_id>/', views.reject_mechanic, name='reject_mechanic'),
    path("cust-logout/", views.customerlogout, name="customerlogout"),
    path("mech-logout/", views.mechaniclogout, name="mechaniclogout"),
    path('registered-customers/', views.registered_customers, name='registered_customers'),
    path('manage_mechanic/', views.manage_mechanic, name='manage_mechanic'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('manage-services/', views.manage_service, name='manage_service'),
    path('view-requests',views.view_requests,name='view_request'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('view-profile/', views.view_profile, name='view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Added Edit Profile URL
    path('view-mechanic-details/', views.view_mechdetails, name='view_mechanic_details'),

    path('assign-task/', views.assign_task, name='assign_task'),
    path('mechanic/appointments/', views.my_appointments, name='my_appointments'),
    path('customer/requests/', views.my_requests, name='my_requests'),
    path('contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('send-messages/', views.see_taskdetails, name='alert_msg'),
    path('send-approve-alerts/', views.approve_msg, name='send_approve_alerts'),
    path('notification-menu/', views.notification_menu, name='notification_menu'),
     path('view-tasks/', views.view_task_details, name='view_task_details'),  # ✅ View all assigned tasks
    path('edit-task-status/<int:task_id>/', views.edit_task_status, name='edit_task_status'),
    path('get-mechanics/', views.get_mechanics_by_district, name='get_mechanics_by_district'),
    path('mechanic/tasks/', views.mechanic_assigned_tasks, name='mechanic_assigned_tasks'),
    path('mechanic/task/<int:task_id>/update/', views.update_mechanic_task_status, name='update_mechanic_task_status'),
    path('work-details/', views.mechanic_work_details, name='mechanic_work_details'),
    path('fill-details/<int:task_id>/', views.fill_mechanic_details, name='fill_mechanic_details'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/fill/<int:service_request_id>/', views.fill_feedback, name='fill_feedback'),
    path('mechanic-details/<int:mechanic_id>/', views.view_byadmin, name='view_byadmin'),
    path('my-payments/', views.payment_page, name='payment_page'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('back-mechdash/', views.backdashboardmech, name='mech_dash'),
    path('past-work/', views.view_pastwork, name='view_pastwork'),
    #  path('admin/work-history/', views.view_workhistbyadmin, name='view_workhistbyadmin'),
]
    # path('mechanic-success/', views.success_reg, name='mechanic_success'),
    # path('task-status', views.add_status, name='update_task_status'),
    # path('mechanic/appointments/', views.assigned_tasks, name='mechanic_assigned_tasks'),
    # path('mechanic/update-task/<int:task_id>/', views.update_mechanic_task_status, name='update_mechanic_task_status'),

     

    # path('task/<int:task_id>/add_status/', views.add_status, name='add_status'),
    # path('task/<int:task_id>/work_details/', views.work_details_filling, name='work_details_filling'),
    
    
    



    

   

