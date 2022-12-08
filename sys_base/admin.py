from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .models import Patient, Doctor, AdminStaff, AppointmentRequest, Specialize, Appointment

# Register your models here.

admin.site.register(Account, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AdminStaff)
admin.site.register(Specialize)
admin.site.register(Appointment)
