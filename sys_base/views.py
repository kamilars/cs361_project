from pydoc import Doc
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorForm, LoginAdminForm, PatientForm, AppointmentForm
from .models import Doctor, AdminStaff, Patient, AppointmentRequest, Appointment, Specialize, Account
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def errormsg(request):
    return render(request, 'sys_base/errormsg.html')

def index(request):
    if 'name' in request.session:
        del request.session['name']
    if 'surname' in request.session:
        del request.session['surname']
    if 'doctor' in request.session:
        del request.session['doctor']
    if 'date' in request.session:
        del request.session['date']
    if 'timeslot' in request.session:
        del request.session['timeslot']
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
def patient_delete(request, id):
    patient = Patient.objects.get(pk=id)
    patient.delete()
    return redirect('/patient_list')

@login_required(login_url='login')
def patient_register(request, id=None):
    if request.method == "GET":
        if id==None:
            form = PatientForm()
        else:
            patient = Patient.objects.get(pk=id)
            form = PatientForm(instance=patient)
        return render(request, "sys_base/patient_form.html", {'form':form})
    elif request.method == "POST":
        if id==None:
            form = PatientForm(request.POST)
        else:
            patient = Patient.objects.get(pk=id)
            form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
        else:
            return redirect('/patient_register')
        return redirect('/patient_list')

def appointment(request, id):
    context={}

    doctor = Doctor.objects.get(pk=id)
    selected_doctor=doctor.name+" "+doctor.surname
    context['doctor_name'] = selected_doctor
    avail_days_row = Appointment.objects.filter(doctor=doctor.pk, status='unscheduled')
    avail_dates = []
    for day in avail_days_row:
        avail_dates.append((day.date, day.date))
    print(f"AVAILABLE DAYS: {avail_dates}")
    #context['form2'] = AppointmentForm(avail_dates, initial={'doctor': doctor.pk})
    context['form2'] = AppointmentForm(initial={'doctor': doctor.pk})
    context['form1'] = PatientForm()

    if request.method == "GET":
        #avail_days = avail_days_row.date
        return render(request, "sys_base/request_app_form.html", context)
    elif request.method == "POST":
        form1 = PatientForm(request.POST)
        form2 = AppointmentForm(request.POST)
        if form1.is_valid():
            iin = form1.cleaned_data['iin']
            name = form1.cleaned_data['name']
            surname = form1.cleaned_data['surname']
            email = form1.cleaned_data['email']
            contact_number = form1.cleaned_data['contact_number']
            Patient.objects.create(iin=iin, name=name, surname=surname, email=email, contact_number=contact_number)
            if form2.is_valid():
                patient_iin = form1.cleaned_data['iin']
                doc = form2.cleaned_data['doctor']
                date = form2.cleaned_data['date']
                timeslot = form2.cleaned_data['timeslot']
                Appointment.objects.update(doctor=doc, patient_iin=patient_iin, date=date, timeslot=timeslot, status='requested')
                request.session['name'] = name
                request.session['surname'] = surname
                request.session['date'] = date
                request.session['timeslot'] = timeslot
                request.session['doctor'] = selected_doctor
                return redirect('/appointment_confirmation')
        else:
            return redirect('/')
            


def requested_appointments(request):
    context = {}
    if request.user.is_superuser:
        context['usertype'] = 'admin'
        appointments = Appointment.objects.all()
        context['appointments'] = appointments
    elif hasattr(request.user, 'doctor'):
        context['usertype'] = 'Doctor'
        appointments = Appointment.objects.filter(doctor__account__username = request.user.username)
        context['appointments'] = appointments
    elif hasattr(request.user, 'patient'):
        context['usertype'] = 'Patient'
        appointments = Appointment.objects.filter(patient__account__username = request.user.username)
        context['appointments'] = appointments
    else:
        context['usertype'] = 'Admin'
        appointments = Appointment.objects.all()
        context['appointments'] = appointments

    return render(request, "sys_base/requested_appointments.html", context)

def appointment_confirmation(request, id=None):
    return render(request, "sys_base/appointment_confirmation.html") #, context)

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
        else:
            return redirect('/doctor_register')
        return redirect('/')

@login_required(login_url='login')
def doctor_delete(request, iin):
    doctor = Doctor.objects.get(pk=iin)
    doctor.delete()
    return redirect('/doctors_list')


def searchdoctors(request):
    context = {}

    doctors = Doctor.objects.all()
    context["doctors"] = doctors
    context["specializations"] = Specialize.objects.order_by().distinct()

    if 'searchbarsubmit' in request.POST:
        q = request.POST.get('searchbardoctors')
        s = request.POST.get('select_spec')
        try:
            if s != "Select from below":
                search = Doctor.objects.filter(specialize__spec__icontains=s)
            else:
                search = Doctor.objects.filter(name = q) | Doctor.objects.filter(surname = q)
            
            paginator = Paginator(search, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj
        except:
            msg = 'error :('
        
    return render(request, 'sys_base/searchdoctors.html', context)