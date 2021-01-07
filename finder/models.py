import datetime
from django.db import models
from django.utils import timezone
import requests
import urllib.parse
from django.conf import settings
import json
import sys

# Create your models here.

class Event(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=200)
    eventtype = models.ForeignKey('finder.EventType', default=1, on_delete=models.CASCADE)
    covidsafetylevel = models.ForeignKey('finder.CovidSafetyLevel', default=1, on_delete=models.CASCADE)
    startdate = models.DateTimeField('event start date', default=timezone.now )
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    username = models.CharField(max_length=50, default='admin')
    remote = models.BooleanField(default=False)
    size = models.IntegerField()
    outdoor = models.BooleanField(help_text='Input only required if event not remote', default=False)
    masks = models.BooleanField(help_text='Input only required if event not remote', default=False)
    distanced = models.BooleanField(help_text='Input only required if event not remote', default=False)

    def __str__(self):
        return self.name

    def was_started_recently(self):
        return self.startdate >= timezone.now() - datetime.timedelta(days=1)

    def calc_safety(self, size, outdoor, masks, distanced, etype, remote):
        safety = 0
        if remote: return 5

        if int(size) <= 10: safety += 1
        if outdoor: safety += 1
        if masks: safety += 1
        if distanced: safety += 1
        if str(etype) == "Study Group" or str(etype) == "Academic Seminar": safety += 1

        return safety

    def save(self, *args, **kwargs):

        clevel = CovidSafetyLevel.objects.get(covidsafetylevel=self.calc_safety(self.size, self.outdoor, self.masks, self.distanced, self.eventtype, self.remote))
        self.covidsafetylevel = clevel

        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

        params = {
            'address': self.address,
            'sensor': 'false',
            'region': 'USA',
            'key': settings.GOOGLE_GEOCODE_API_KEY
        }

        # Do the request and get the response data
        try:
            req = requests.get(GOOGLE_MAPS_API_URL, params=params)
            res = req.json()

            # Use the first result
            result = res['results'][0]

            self.latitude = result['geometry']['location']['lat']
            self.longitude = result['geometry']['location']['lng']
        except:
            self.latitude = 38.0335529
            self.longitude = -78.5079772

        super(Event, self).save(*args, **kwargs)
    
class EventType(models.Model):
    eventtype = models.CharField(max_length=50)

    class Meta:
        ordering = ['eventtype']

    def __str__(self):
        return self.eventtype

class CovidSafetyLevel(models.Model):
    covidsafetylevel = models.CharField(max_length=2)

    class Meta:
        ordering = ['covidsafetylevel']

    def __str__(self):
        return self.covidsafetylevel

class Registration(models.Model): 
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    guests = models.IntegerField(default=1)
    confirmationno = models.CharField(max_length=50, default='1ABCDEFGH')
    event = models.ForeignKey('finder.Event', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.fname, self.lname)
