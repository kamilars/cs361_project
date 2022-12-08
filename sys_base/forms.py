from django import forms
from django.forms import ModelForm, HiddenInput
from .models import Doctor
from .models import AdminStaff
from .models import Patient
from .models import AppointmentRequest
from .models import Appointment
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
            'photo_doctor':'Photo',
            'specialization_details_id':'Specialization'
        }

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        SPECIALIZATIONS_LIST = (
            ('Allergist', 'Allergist'),
            ('Cardiologist', 'Cardiologist'),
            ('Dermatologists', 'Dermatologist'),
            ('Endocrinologist', 'Endocrinologist'),
            ('Physician', 'Physician'),
            ('Gastroenterologist', 'Gastroenterologist'),
        )
        years=[]
        for year in range(1940,2021):
            years.append(year)
        years.reverse()
        self.fields["date_of_birth"].widget = forms.SelectDateWidget(years=years, empty_label=("Year", "Month", "Day"))
        self.fields["specialization_details_id"].widget = forms.Select(choices=SPECIALIZATIONS_LIST)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('__all__')
        labels = {
            'iin':'IIN',
        }

        def clean_iin(self, *args, **kwargs):
            iin = self.cleaned_data.get('iin')
            print('IIN: ', iin)
            if len(iin) == 12:
                return iin
            else:
                raise forms.ValidationError({'iin':'IIN length should be 12'})
    
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['middlename'].required = False
        years=[]
        for year in range(1940,2021):
            years.append(year)
        years.reverse()
        self.fields["date_of_birth"].widget = forms.TextInput( attrs={'type': 'date'} )
        self.fields["email"].widget = forms.EmailInput()


class LoginAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AdminStaff
        fields={'username', 'password'}

class AppointmentRequest(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ('patient_name', 'patient_surname', 'contact', 'doctor', 'time_slot')
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("__all__")
    def __init__(self, dates, *args, **kwargs):
        if isinstance(dates, list):
            super(AppointmentForm, self).__init__(*args, **kwargs)
            AVAIL_DATES = dates
            self.fields["date"].widget = forms.Select(choices=AVAIL_DATES)
        self.fields['patient_iin'].widget = HiddenInput()
        self.fields['status'].widget = HiddenInput()
        self.fields['doctor'].widget = HiddenInput()
        self.fields["timeslot"].widget = forms.Select()   

class AppointmentForm1(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("__all__")
    def __init__(self, dates, *args, **kwargs):
        if isinstance(dates, list):
            super(AppointmentForm1, self).__init__(*args, **kwargs)
            AVAIL_DATES = dates
            self.fields["date"].widget = forms.Select(choices=AVAIL_DATES)
        self.fields['patient_iin'].widget = HiddenInput()
        self.fields['patient'].widget = HiddenInput()
        self.fields['status'].widget = HiddenInput()
        self.fields['doctor'].widget = HiddenInput()
        self.fields["timeslot"].widget = forms.Select()   


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("__all__")
    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['patient_iin'].widget = HiddenInput()
        self.fields['status'].widget = HiddenInput()
        self.fields['doctor'].widget = HiddenInput() 
        self.fields['patient'].widget = HiddenInput() 
        self.fields['date'].widget = HiddenInput() 
        self.fields['timeslot'].widget = HiddenInput() 