from django.contrib import admin
from .models import Patient, Doctor, AdminStaff, AppointmentRequest, Specialize, Appointment

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AdminStaff)
<<<<<<< HEAD
admin.site.register(AppointmentRequest)
=======
>>>>>>> 113e9c1e38475f4c88bbb7dd4ff2144ca471d906
admin.site.register(Specialize)
admin.site.register(Appointment)
