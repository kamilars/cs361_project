from django.contrib import admin
from .models import Patient, Doctor, AdminStaff, AppointmentRequest, Specialize, Appointment

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AdminStaff)
admin.site.register(AppointmentRequest)
admin.site.register(Specialize)
admin.site.register(Appointment)
