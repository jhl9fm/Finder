from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from .models import Event, EventType, CovidSafetyLevel, Registration
from .forms import EventForm
from .forms import RegistrationForm
import time
import datetime
from django.conf import settings
from django.core.mail import send_mail
import string 
import random 

# Create your views here.
def home(request):
    return render(request, "finder/index.html")

def eventlist(request):
    events_list = Event.objects.all()
    event = Event()
    context = {'events_list': events_list,
               'event': event,
               'api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'finder/map.html', context)

def map(request, id):
    events_list = Event.objects.all
    event = get_object_or_404(Event, pk=id)
    context = {'events_list': events_list,
               'event': event,
               'api_key': settings.GOOGLE_MAPS_API_KEY
    }

    return render(request, 'finder/map.html', context)
    
def about(request):
    return render(request, "finder/about.html")

def contact(request):
    return render(request, "finder/contact.html")

def logout(request):
    return render(request, "finder/logout.html")

def add_event(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EventForm()
            header = 'Finder : Add Event'
        else:
            event = Event.objects.get(pk=id)
            form = EventForm(instance=event)
            header = 'Finder : Update Event'

        context = {'form': form,
                   'header': header, 
            }

        return render(request, "finder/add_event.html", context)
    else:
        if id == 0:
            form = EventForm(request.POST)
        else:
            event = Event.objects.get(pk=id)
            form = EventForm(request.POST, instance=event)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user.username
            obj.save()

        return redirect('/event_list')

def search(request):
    if request.method=="POST":
        etype=request.POST.get('eventtype')
        clevel=request.POST.get('covidsafetylevel')
        dateopt = request.POST.get('dateopt')
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')

        if(date1 == ''):
            dateopt = 'all'
        if(date2 == '' and dateopt=='between'):
            dateopt = 'all'

        level=CovidSafetyLevel.objects.get(covidsafetylevel=clevel)
        if(etype=='all'):
            events_list=Event.objects.all().filter(covidsafetylevel__gte = level.id)
        else:
            type=EventType.objects.get(eventtype=etype)
            events_list=Event.objects.all().filter(eventtype=type.id).filter(covidsafetylevel__gte=level.id) 

        if(dateopt == 'on'):
            events_list = events_list.filter(startdate__gte = datetime.datetime.strptime(date1, '%Y-%m-%d')).filter(startdate__lte = (datetime.datetime.strptime(date1, '%Y-%m-%d')  + datetime.timedelta(days=1)))          
        elif(dateopt == 'before'):
            events_list = events_list.filter(startdate__lte = (datetime.datetime.strptime(date1, '%Y-%m-%d') + datetime.timedelta(days=1)))          
        elif(dateopt == 'after'):
            events_list = events_list.filter(startdate__gte = datetime.datetime.strptime(date1, '%Y-%m-%d'))          
        elif(dateopt == 'between'):
            events_list = events_list.filter(startdate__gte = datetime.datetime.strptime(date1, '%Y-%m-%d')).filter(startdate__lte = (datetime.datetime.strptime(date2, '%Y-%m-%d')  + datetime.timedelta(days=1)))          
        else:
            pass


        event = Event()
        context = {'events_list': events_list,
               'event': event,
               'api_key': settings.GOOGLE_MAPS_API_KEY
        }

        return render(request, 'finder/map.html', context)
    else:
        types=EventType.objects.all() 
        covidlevels=CovidSafetyLevel.objects.all()
        context = {'types': types,
                   'covidlevels': covidlevels 
        }

        return render(request, 'finder/eventsearch.html', context)

def detail(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {'event': event
        }

    return render(request, 'finder/detail.html', context)

def event_list(request):
    context = {'event_list': Event.objects.all().filter(username=request.user.username)}
    return render(request, "finder/event_list.html", context)

def event_delete(request,id):
    event = Event.objects.get(pk=id)
    event.delete()
    return redirect('/event_list')

def reg_event(request, id):
    if request.method == "GET":

        form = RegistrationForm()

        form.fields["event"].initial = id
        form.fields["fname"].initial = request.user.first_name
        form.fields["lname"].initial = request.user.last_name
        form.fields["email"].initial = request.user.email


        context = {'form': form,
            }

        return render(request, "finder/registration.html", context)

    else:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            # initializing size of string  
            N = 10
  
            # using random.choices() 
            # generating random strings  
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N)) 
            obj.confirmationno = res
            obj.save()

            event = Event.objects.get(pk=id)
            subject = 'Event Registration'
            body = 'You registered for ' + event.name + '\r\n' + 'Address : ' + event.address + '\r\nDate : ' + str(event.startdate) + '\r\n\r\nThe confirmation number is ' + res
            sender = 'i22.uva2020@gmail.com'
            to = [request.user.email,] 
            
            send_mail(
                subject,
                body,
                sender,
                to,
            )

        return redirect('/reg_list')


def reg_list(request):
    context = {'reg_list': Registration.objects.all().filter(email=request.user.email)}
    return render(request, "finder/reg_list.html", context)

def reg_delete(request,id):
    reg = Registration.objects.get(pk=id)
    reg.delete()
    return redirect('/reg_list')
