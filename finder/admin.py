from django.contrib import admin

# Register your models here.

from finder import models
from .models import Event
from .models import EventType
from .models import CovidSafetyLevel

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(CovidSafetyLevel)