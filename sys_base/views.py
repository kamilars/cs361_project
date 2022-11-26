from pydoc import Doc
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorForm, LoginAdminForm, PatientForm
from .models import Doctor, Admin, Patient
# Create your views here.

def errormsg(request):
    return render(request, 'sys_base/errormsg.html')

def index(request):
    #doctors_list = Doctor.objects.order_by('-name')[:5]
    #context = {'doctors': doctors_list}
    return render(request, 'sys_base/index.html')

def login(request):
    form = LoginAdminForm()
    return render(request, "sys_base/login.html", {'form':form})

def admin_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        admin=Admin.objects.filter(username=username, password=password).count()
        if admin>0:
            msg='Successful'
        else:
            msg='Invalid :('
    form=LoginAdminForm
    return render(request, 'sys_base/admin.html')

def patient_list(request):
    context = {'patient_list':Patient.objects.all()}
    return render(request, "sys_base/patient_list.html", context)

def patient_delete(request, iin):
    patient = Patient.objects.get(pk=iin)
    patient.delete()
    return redirect('/patient_list')

def patient_register(request, iin=None):
    if request.method == "GET":
        if iin==None:
            form = PatientForm()
        else:
            patient = Patient.objects.get(pk=iin)
            form = PatientForm(instance=patient)
        return render(request, "sys_base/patient_form.html", {'form':form})
    elif request.method == "POST":
        if iin==None:
            form = PatientForm(request.POST)
        else:
            patient = Patient.objects.get(pk=iin)
            form = DoctorForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
        return redirect('/patient_list')
   

def doctor_delete(request, iin):
    doctor = Doctor.objects.get(pk=iin)
    doctor.delete()
    return redirect('/doctors_list')