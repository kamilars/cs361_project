from pydoc import Doc
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorForm, LoginAdminForm, PatientForm, AppointmentForm, PrescriptionForm
from .models import Doctor, AdminStaff, Patient, AppointmentRequest, Appointment, Specialize, Account
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
# Create your views here.

def errormsg(request):
    return render(request, 'sys_base/errormsg.html')

def index(request):
    context = {}
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
    context = {'doctor_id': 1}
    return render(request, 'sys_base/index.html', context)

def base(request):
    context = {}
    context = {'doctor_id': 1}
    return render(request, 'sys_base/base.html', context)

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

def load_timeslots(request):
    date = request.GET.get('date')
    doctorId = request.GET.get('doctorId')
    timeslots_entries = Appointment.objects.filter(date=date, doctor=doctorId, status='unscheduled')
    timeslots = []
    for timeslot_entry in timeslots_entries:
            #timeslots.append((timeslot_entry.timeslot, timeslot_entry.timeslot))
        timeslots.append (timeslot_entry.timeslot)
    print(f"TIMESLOTS CHOSEN FROM AJAX: {timeslots}")
    return render(request, 'sys_base/timeslots_dropdown_list_options.html', {'timeslots':timeslots})



def appointment(request, id):
    context={}
    doctor = Doctor.objects.get(pk=id)
    selected_doctor=doctor.name+" "+doctor.surname
    context['doctor_name'] = selected_doctor
    avail_days_row = Appointment.objects.filter(doctor=doctor.pk, status='unscheduled').order_by('date')
    dates_distinct = set()
    for day in avail_days_row:
        dates_distinct.add(day.date)
    avail_dates = []
    for day in dates_distinct:
        avail_dates.append((day, day))
    context['form2'] = AppointmentForm(avail_dates, initial={'doctor': doctor.pk, 'status': 'requested'})   
    if request.user.is_authenticated and request.user.patient:
        context['form1'] = PatientForm(initial={'iin':request.user.patient.iin, 'name' : request.user.patient.name,
        'surname' : request.user.patient.surname, 'email' : request.user.patient.email, 'contact_number' : request.user.patient.contact_number})
    else:
        context['form1'] = PatientForm()

    if request.method == "GET":
        return render(request, "sys_base/request_app_form.html", context)
    elif request.method == "POST":
        form1 = PatientForm(request.POST)
        form2 = AppointmentForm(avail_dates, request.POST)
        print(f"FORM1: {form1}")
        if form1.is_valid():
            iin = form1.cleaned_data['iin']
            name = form1.cleaned_data['name']
            surname = form1.cleaned_data['surname']
            email = form1.cleaned_data['email']
            contact_number = form1.cleaned_data['contact_number']
            for field in form2:
                print("Field Error:", field.name, field.errors)
            pat = Patient.objects.create(iin=iin, name=name, surname=surname, email=email, contact_number=contact_number)
            doc = request.POST['doctor']
            date = request.POST['date']
            timeslot = request.POST['timeslot']
            app = Appointment.objects.get(doctor=doc,date=date, timeslot=timeslot)
            app.patient = pat
            app.patient_iin = request.POST['iin']
            app.status = 'requested'
            app.save()
            request.session['name'] = name
            request.session['surname'] = surname
            request.session['date'] = date
            request.session['timeslot'] = timeslot
            request.session['doctor'] = selected_doctor
            return redirect('/appointment_confirmation')
        else:
            return redirect('/')            

def app_confirm(request, id):
    app = Appointment.objects.get(pk=id)
    app.status = 'confirmed'
    app.save()
    return redirect('/requested_appointments')
    
def makeprescription(request, id):
    context = {}
    app = Appointment.objects.get(pk=id)
    context['patient'] = Patient.objects.get(iin=app.patient_iin)
    if request.method == "GET":
        context['form'] = PrescriptionForm(instance=app)
        return render(request, "sys_base/makeprescription.html", context)
    else:
        app.status = 'finished'
        app.prescription = request.POST['prescription']
        app.save()
        return redirect('/requested_appointments')

def patient_app_request(request, id):
    context = {}
    doctor = Doctor.objects.get(pk=id)
    selected_doctor=doctor.name+" "+doctor.surname
    context['doctor_name'] = selected_doctor
    avail_days_row = Appointment.objects.filter(doctor=doctor.pk, status='unscheduled').order_by('date')
    dates_distinct = set()
    for day in avail_days_row:
        dates_distinct.add(day.date)
    avail_dates = []
    for day in dates_distinct:
        avail_dates.append((day, day))
    context['form2'] = AppointmentForm(avail_dates, initial={'doctor': doctor.pk, 'status': 'requested'}) 
    if request.method == "GET":
        return render(request, "sys_base/patient_app_request", context)
    elif request.method == "POST":
        form2 = AppointmentForm(avail_dates, request.POST)
        if form2.is_valid():
            return redirect('/appointment_confirmation')
    return render(request, 'sys_base/patient_app_request', context)

def requested_appointments(request):
    context = {}
    if request.user.is_superuser:
        context['usertype'] = 'admin'
        appointments = Appointment.objects.filter(status='requested')
        context['appointments'] = appointments
    elif hasattr(request.user, 'doctor'):
        context['usertype'] = 'Doctor'
        appointments = Appointment.objects.filter(doctor__account__username = request.user.username, status='confirmed')
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
        splitname = q.split(" ")
        print(f"SPLITTED NAME: {splitname}")
        s = request.POST.get('select_spec')
        try:
            if s != "Select from below":
                search = Doctor.objects.filter(specialize__spec__icontains=s)
            else:
                search = Doctor.objects.filter(name = q) | Doctor.objects.filter(surname = q)
                if len(splitname) == 2:
                    search = Doctor.objects.filter(name = splitname[1], surname = splitname[0])
            
            paginator = Paginator(search, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj
        except:
            msg = 'error :('
        
    return render(request, 'sys_base/searchdoctors.html', context)



def doctor_schedulemanager(request, id=None):
    context={}
    TIMESLOT_LIST = [
        '09:00 – 09:20',
        '09:30 – 09:50',
        '10:00 – 10:20',
        '10:30 – 10:50',
        '11:00 – 11:30',
        '11:30 – 11:50',
        '12:00 – 12:20',
        '12:30 – 12:50',
        '14:00 – 14:20',
        '14:30 – 14:50'
    ]
    DATE_LIST=[]
    DATE_LIST_FORMATTED = []
    for i in range(0,7):
        day = date.today() + timedelta(days=i)
        DATE_LIST.append(str(day))
        DATE_LIST_FORMATTED.append(day.strftime("%b %d"))
    context['timeslots'] = TIMESLOT_LIST
    context['dates'] = DATE_LIST
    context['dates_f'] = DATE_LIST_FORMATTED

    slots=[]
    if request.POST:
        for each in request.POST:
            slots.append(each)

        del slots[0]
        del slots[-1]

        slots_spl = []

        for each in slots:
            slots_spl.append(each.split('_'))
        
        doctorId=1
        for each in slots_spl:
            doc=Doctor.objects.get(pk=1)
            app = Appointment.objects.create(doctor=doc,date=each[0], timeslot=each[1])
            app.timeslot = each[1]
            app.save()
        return redirect('/')

    #print(f"SLOTS: {slots_spl}")
    
    return render(request, 'sys_base/doctor_schedulemanager.html', context)

