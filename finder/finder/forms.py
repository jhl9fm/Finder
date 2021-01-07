from django import forms
from .models import Event
from .models import Registration

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'address', 'eventtype',
            'startdate', 'remote', 'size', 'outdoor', 'masks', 'distanced')
        labels = {
            'name':'Name',
            'description':'Description',
            'address':'Address',
            'eventtype':'Event Type',
            'startdate':'Start Date (MM/DD/YYYY HH:MM)',
            'remote':'Event is remote',
            'size':'Max attendees allowed',
            'outdoor':'Event is outdoor',
            'masks':'Masks required',
            'distanced':'Social distancing required',
        }
                
        widgets = {'startdate': forms.DateTimeInput(format='%m/%d/%Y %H:%M', attrs={'class':'datetimefield'}),  }

    def __init__(self, *args, **kwargs):
        super(EventForm,self).__init__(*args, **kwargs)
        #self.fields['startdate'].required = True

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ( 'event', 'fname', 'lname', 'email', 'confirmationno' )
        labels = {
            'enent':'Event',
            'fname':'First Name',
            'lname':'Last Name',
            'email':'Email',
        }

        widgets = {'confirmationno': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['readonly'] = True
        self.fields['fname'].widget.attrs['readonly'] = True
        self.fields['lname'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
