from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('searchdoctors/', views.searchdoctors, name='searchdoctors'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient/<str:iin>/', views.patient_register, name='patient_update'),
    path('patient/delete/<str:iin>/', views.patient_delete, name='patient_delete'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('request_appointment/<int:id>', views.request_appointment, name='request_appointment'),
    path('errormsg/', views.errormsg, name='errormsg')    
]