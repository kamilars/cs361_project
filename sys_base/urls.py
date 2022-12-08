from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('searchdoctors/', views.searchdoctors, name='searchdoctors'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient/<str:id>/', views.patient_register, name='patient_update'),
    path('patient/delete/<str:id>/', views.patient_delete, name='patient_delete'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('request_appointment/<int:id>', views.appointment, name='request_appointment'),
    path('appointment_confirmation/', views.appointment_confirmation, name='appointment_confirmation'),
    path('requested_appointments/', views.requested_appointments, name='requested_appointments'),
    path('patient_app_request/<int:id>', views.patient_app_request, name='patient_app_request'),
    path('doctor_schedulemanager/<int:id>', views.doctor_schedulemanager, name='doctor_schedulemanager'),
    path('ajax/load-timeslots', views.load_timeslots, name='ajax_load_timeslots')
]