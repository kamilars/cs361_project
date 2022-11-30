from django.contrib import admin
<<<<<<< HEAD
from .models import Patient, Doctor, AdminStaff, AppointmentRequest, Specialize
=======
from .models import Patient, Doctor, AdminStaff, AppointmentRequest,Appointment
>>>>>>> b38921cb681ed0c6702966637d4010be8633b0ef

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AdminStaff)
<<<<<<< HEAD
admin.site.register(AppointmentRequest)
admin.site.register(Specialize)
=======
#admin.site.register(AppointmentRequest)
admin.site.register(Appointment)
>>>>>>> b38921cb681ed0c6702966637d4010be8633b0ef
