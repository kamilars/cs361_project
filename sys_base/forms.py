from django import forms
from .models import Doctor
from .models import AdminStaff
from .models import Patient
from .models import AppointmentRequest
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('iin', 'name', 'middlename', 'surname', 'date_of_birth', 'contact_number', 'department_id', 'specialization_details_id', 'experience', 'photo_doctor', 'category_doctor', 'price_of_appointment', 'schedule_details', 'degree', 'rating', 'address_doctor')
        labels = {
            'iin':'IIN',
            'address_doctor':'Address',
            'photo_doctor':'Photo'
        }
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        years=[]
        for year in range(1940,2021):
            years.append(year)
        years.reverse()
        self.fields["date_of_birth"].widget = forms.SelectDateWidget(years=years, empty_label=("Year", "Month", "Day"))


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('__all__')
        def __init__(self, *args, **kwargs):
            super(PatientForm, self).__init__(*args, **kwargs)
            self.fields['middlename'].required = False

class LoginAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AdminStaff
        fields={'username', 'password'}

class AppointmentRequest(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ('patient_name', 'patient_surname', 'contact', 'doctor', 'time_slot')