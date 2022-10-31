from pydoc import Doc
from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctor
# Create your views here.

def index(request):
    doctors_list = Doctor.objects.order_by('-name')[:5]
    context = {'doctors': doctors_list}
    return render(request, 'form.html', context)
