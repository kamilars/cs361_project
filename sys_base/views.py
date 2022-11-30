from pydoc import Doc
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorForm, LoginAdminForm, PatientForm, AppointmentRequest
from .models import Doctor, AdminStaff, Patient
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def errormsg(request):
    return render(request, 'sys_base/errormsg.html')

def index(request):
    #doctors_list = Doctor.objects.order_by('-name')[:5]
    #context = {'doctors': doctors_list}
    return render(request, 'sys_base/index.html')


def loginpage(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username)
        except:
            msg = 'User does not exist'

        user = authenticate(request, username = username, password = password)

        if user is not None:
            context['user'] = username
            login(request, user)
            return redirect('index')
        else:
            msg = 'User does not exist or password is incorrect'

    form = LoginAdminForm()
    context['form'] = form
    context.update
    return render(request, "sys_base/login.html", context)


@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('index')


def admin_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        admin=AdminStaff.objects.filter(username=username, password=password).count()
        if admin>0:
            msg='Successful'
        else:
            msg='Invalid :('
    form=LoginAdminForm
    return render(request, 'sys_base/admin.html')

@login_required(login_url='login')
def patient_list(request):
    context = {'patient_list':Patient.objects.all()}
    return render(request, "sys_base/patient_list.html", context)

@login_required(login_url='login')
def patient_delete(request, iin):
    patient = Patient.objects.get(pk=iin)
    patient.delete()
    return redirect('/patient_list')

@login_required(login_url='login')
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
            form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
        return redirect('/patient_list')

#@login_required(login_url='login')
def request_appointment(request, id=None):
    if request.method == "GET":
        if id==None:
            form = AppointmentRequest()
        else:
            doctor = Doctor.objects.get(pk=id)
            selected_doctor=doctor.name+" "+doctor.surname
            form = AppointmentRequest(initial={'doctor': selected_doctor})
        return render(request, "sys_base/request_app_form.html", {'form':form})
    elif request.method == "POST":
        form = AppointmentRequest(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')


@login_required(login_url='login')
def doctor_register(request, iin=None):
    if request.method == "GET":
        if iin==None:
            form = DoctorForm()
        else:
            doctor = Doctor.objects.get(pk=iin)
            form = DoctorForm(instance=doctor)
        return render(request, "sys_base/doctor_form.html", {'form':form})
    elif request.method == "POST":
        if iin==None:
            form = DoctorForm(request.POST)
        else:
            doctor = Doctor.objects.get(pk=iin)
            form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/index')

@login_required(login_url='login')
def doctor_delete(request, iin):
    doctor = Doctor.objects.get(pk=iin)
    doctor.delete()
    return redirect('/doctors_list')


def searchdoctors(request):
    context = {}

    if 'searchbarsubmit' in request.POST:
        q = request.POST.get('searchbar')
        try:
            search = Doctor.objects.filter(name = q) | Doctor.objects.filter(surname = q)
            paginator = Paginator(search, 3)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {'page_obj' : page_obj}
        except:
            msg = 'error :('

    return render(request, 'sys_base/searchdoctors.html', context)