from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('doctor/', views.doctor_reg, name='doctor_register'),
    path('login/', views.login, name='login'),
    #path('admin/', views.admin_login, name="admin_login"),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient/<str:iin>/', views.patient_register, name='patient_update'),
    path('patient/delete/<str:iin>/', views.patient_delete, name='patient_delete'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('errormsg/', views.errormsg, name='errormsg')
    #path('user/<str:email>/', views.user_form, name='user_update'),
    #path('user/delete/<str:email>/', views.user_delete, name='user_delete'),
    
]