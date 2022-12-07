import code
from email.policy import default
from datetime import datetime, date, timedelta
from msilib.schema import Class
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#Validators
def charfield_is_number_validator(value):
    if value.isdigit():
        return value
    else:
        raise ValidationError('Input contains unacceptable characters')

def blood_type_validator(input):
    if input.upper() != 'A+' or 'A-' or 'B+' or 'B-' or 'O+' or 'O-' or 'AB+' or 'AB-':
        raise ValidationError(
            _('%(input)s contain unacceptable input'),
            params={'value':input},
        )
# Create your models here.

class Account(AbstractUser):
    pass

class AdminStaff(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)

class AppointmentRequest(models.Model):
    requestId = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length = 50)
    patient_surname = models.CharField(max_length = 50)
    contact = models.CharField(max_length = 50)
    doctor = models.CharField(max_length = 100)
    time_slot = models.CharField(max_length = 50)
    status = models.CharField(max_length=20, default="not considered")


class Patient(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    iin = models.CharField(unique=True, default='', max_length = 12, validators = [validators.MinLengthValidator(12), charfield_is_number_validator])
    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    middlename = models.CharField(max_length = 30, blank=True, default='')
    blood_group = models.CharField(max_length = 3, blank=True) #, validators = [blood_type_validator])
    contact_number = models.CharField(
        blank=True,
        max_length = 11, 
        validators = [
            validators.RegexValidator(
                "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$",
                message = "Incorrect Phone Number"
            ), 
            validators.MinLengthValidator(11)
        ]
    )
    email = models.CharField(blank=True, max_length = 30 ,validators = [validators.EmailValidator])
    address = models.CharField(blank=True, max_length = 30)
    marital_status = models.CharField(max_length = 30,blank=True)
    registration_date = models.DateField(auto_now_add = True)

    def __str__(self):
        return "%s %s" % (self.surname, self.name)


class Doctor(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField()
    iin = models.CharField(max_length = 12, validators = [validators.MinLengthValidator(12), charfield_is_number_validator])
    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    middlename = models.CharField(max_length = 30, blank=True, default='')
    contact_number = models.CharField(
        max_length = 11, 
        validators = [
            validators.RegexValidator(
                "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$",
                message = "Incorrect Phone Number"
            ), 
            validators.MinLengthValidator(11)
        ]
    )
    department_id = models.PositiveIntegerField()
    specialization_details_id = models.CharField(max_length = 30)
    experience = models.PositiveIntegerField(validators = [validators.MaxValueValidator(100)])
    photo_doctor = models.ImageField(upload_to = 'imgs/', null=True, default = 'null')
    category_doctor = models.CharField(max_length = 10)
    price_of_appointment = models.PositiveIntegerField()
    schedule_details = models.CharField(max_length = 30) 
    degree = models.CharField(max_length = 10)
    rating = models.DecimalField(decimal_places = 1, max_digits = 2 ,validators = [validators.MinValueValidator(0.0), validators.MaxValueValidator(10.0)])
    address_doctor = models.CharField(max_length = 30, blank=True)
    def __str__(self):
        return "Dr. %s %s" % (self.surname, self.name)


class Specialize(models.Model):

    SPECIALIZATIONS_LIST = (
        ('Allergist', 'Allergist'),
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologists', 'Dermatologist'),
        ('Endocrinologist', 'Endocrinologist'),
        ('Physician', 'Physician'),
        ('Gastroenterologist', 'Gastroenterologist'),
    )

    doctor_id = models.OneToOneField(
        'Doctor', 
        db_column='iin',
        on_delete=models.CASCADE,
        primary_key=True)
    spec = models.CharField(max_length=30, choices=SPECIALIZATIONS_LIST, default='Allergist')

    def __str__(self):
        return"Specialization: %s" % (self.spec)


class Appointment(models.Model):

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')

    TIMESLOT_LIST = (
        ('09:00 – 09:30', '09:00 – 09:30'),
        ('10:00 – 10:30', '10:00 – 10:30'),
        ('11:00 – 11:30', '11:00 – 11:30'),
        ('12:00 – 12:30', '12:00 – 12:30'),
        ('13:00 – 13:30', '13:00 – 13:30'),
        ('14:00 – 14:30', '14:00 – 14:30'),
        ('15:00 – 15:30', '15:00 – 15:30'),
        ('16:00 – 16:30', '16:00 – 16:30'),
        ('17:00 – 17:30', '17:00 – 17:30'),
    )

    '''DATE_LIST=[]
    for i in range(0,7):
        day = date.today() + timedelta(days=i)
        DATE_LIST.append((str(day), str(day)))'''
   
   
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient_iin = models.CharField(max_length=60, blank=True)
    date = models.CharField(max_length=60)
    timeslot = models.CharField(choices=TIMESLOT_LIST, max_length=60)
    prescription = models.TextField(blank=True)
    status = models.CharField(blank=True, default='unscheduled', max_length=30)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1], self.DATE_LIST[self.date][1]





    


